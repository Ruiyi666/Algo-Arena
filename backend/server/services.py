import threading

# from django.core.cache import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Strategy, Game, Player, FrameAction, FrameState
from .serializers import GameSerializer
from .environments import GameEnvironment, TerritoryTile


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


class GameServer:
    def __init__(self, room_id, max_n_players=2):
        self.life = GameState()
        self.environment: GameEnvironment = GameEnvironment()
        self.meta = {
            "room_id": room_id,
            "map_size": 9,
            "max_players": max_n_players,
            "num_players": 0,
            "frequency": 6,
        }

        self.room_id = room_id
        self.game_id = Game.objects.create(meta=self.meta).id

        self.players = []
        self.states = []
        self.actions = []
        self.recent_action = {}

    @property
    def group_name(self):
        return self.room_id

    def empty(self):
        return len(self.players) == 0

    def full(self):
        return len(self.players) == self.max_n_players

    def save_frame_action(self, frame: int, player_id: int, action: dict):
        FrameAction.objects.create(frame=frame, player_id=player_id, action=action)

    def save_frame_state(self, frame: int, state: dict):
        FrameState.objects.create(frame=frame, state=state, game_id=self.game_id)

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
        self.environment.step(game_action)
        self.broadcast("sync.game.action", game_action)

    def broadcast_game_state(self):
        game = Game.objects.get(id=self.game_id)
        game_state = GameSerializer(game).data
        self.environment.set(game_state)
        self.broadcast("sync.game.state", game_state)

    def broadcast(self, type, content):
        async_to_sync(get_channel_layer().group_send)(
            self.room_id, {"type": type, "content": content}
        )


class GameServerFactory(object):
    @classmethod
    def create(cls, room_id: int) -> GameServer:
        return GameServer(room_id)

    @classmethod
    def destroy(cls, instance: GameServer):
        pass


class GameServerRegistry(object):
    _instances = {}

    @classmethod
    def register(cls, room_id):
        if room_id not in cls._instances.keys():
            cls._instances[room_id] = {
                "instance": GameServerFactory.create(room_id),
                "counter": 0,
            }
        cls._instances[room_id]["counter"] += 1
        return cls._instances[room_id]["instance"]

    @classmethod
    def available(cls, room_id):
        return room_id not in cls._instances.keys()

    @classmethod
    def unregister(cls, room_id):
        if room_id not in cls._instances.keys():
            return

        cls._instances[room_id]["counter"] -= 1
        if cls._instances[room_id]["counter"] == 0:
            GameServerFactory.destroy(
                cls._instances[room_id]["server"],
            )
            cls._instances.pop(room_id)
