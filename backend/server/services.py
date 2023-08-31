import threading
from enum import Enum
from django.core.cache import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Strategy, Game, Player, FrameAction
from .serializers import GameSerializer


class GameState:
    def __init__(self) -> None:
        self._started = False
        self._paused = False

    def started(self):
        return self._started

    def running(self):
        return self._started and not self._paused

    def start(self):
        if self._started:
            raise ValueError("Game has already started or is in an invalid state.")
        self._started = True

    def pause(self):
        if not self._started:
            raise ValueError("Game is not in progress")
        if self._paused:
            raise ValueError("Game cannot be paused.")
        self._paused = True

    def resume(self):
        if not self._started:
            raise ValueError("Game is not in progress")
        if not self._paused:
            raise ValueError("Game cannot be resume.")
        self._paused = False

    def end(self):
        if not self._started:
            raise ValueError("Game is not started.")
        self._started = False


class GameService:
    def __init__(self, room_id, max_n_players=2):
        self.gamestate = GameState()

        self.meta = {
            "room_id": room_id,
            "map_size": 9,
            "max_n_players": max_n_players,
            "player_count": 0,
            "frequency": 6,
        }

        self.room_id = room_id
        self.game_id = Game.objects.create(meta=self.meta).id

        self.players = []  # GamePlayer
        self.actions = []
        self.recent_action = {}

    def empty(self):
        return len(self.players) == 0

    def full(self):
        return len(self.players) == self.max_n_players

    def save_and_close(self):
        for action in self.actions:
            pass
        cache.delete(self.room_id)

    def save_to_cache(self):
        cache.set(self.room_id, self, None)

    @staticmethod
    def load_from_cache(room_id):
        return cache.get(room_id)

    def start_game_timer(self):
        self.game_timer = threading.Timer(
            1 / self.frequency,
            self.broadcase_game_action,
        )
        self.game_timer.start()

    def stop_game_timer(self):
        if self.game_timer:
            self.game_timer.cancel()
            self.game_timer = None

    def start(self):
        if not self.gamestate.started():
            self.gamestate.start()
            self.start_game_timer()

    def end(self):
        if self.gamestate.started():
            self.gamestate.end()
            self.stop_game_timer()

    def create_player(self, strategy_id):
        if self.full():
            return None

        if not self.gamestate.started():
            strategy = Strategy.objects.get(id=strategy_id)
            player_id = Player.objects.create(
                game_id=self.game_id, strategy=strategy
            ).id
            self.players.append(player_id)
            self.broadcast_game_state()
            return player_id
        else:
            raise ValueError("Cannot add a player once the game has started.")

    def destory_player(self, player_id):
        if player_id in self.players:
            if not self.gamestate.started():
                Player.objects.get(id=player_id).delete()
                self.players.remove(player_id)
            elif self.gamestate.ended():
                self.players.remove(player_id)
            else:
                raise ValueError("Game started or cannot found the player_id")
        self.broadcast_game_state()

        if self.empty():
            self.save_and_close()

    def add_action(self, player_id, action):
        self.recent_action[player_id] = action

    def collect_action(self):
        actions = self.recent_action.copy()
        self.recent_action.clear()
        self.actions.append(actions)
        return actions

    def broadcase_game_action(self):
        game_action = self.collect_action()
        self.broadcast("sync.game.action", game_action)

    def broadcast_game_state(self):
        game = Game.objects.get(id=self.game_id)
        game_state = GameSerializer(game).data
        self.broadcast("sync.game.state", game_state)

    def broadcast(self, type, content):
        async_to_sync(get_channel_layer().group_send)(
            self.room_id, {"type": type, "content": content}
        )
