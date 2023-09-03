import asyncio
from asgiref.sync import sync_to_async
# from django.core.cache import cache
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from .models import Strategy, Game, Player, FrameAction, FrameState
from .serializers import (
    FrameStateSerializer,
    FrameActionSerializer,
    PlayerSerializer,
    StrategySerializer,
    GameSerializer
)

from .environments import GameEnvironment, TerritoryTile


class GameState:
    def __init__(self) -> None:
        # waitting -> started[running, paused] -> ended
        self._started = False
        self._ended = False
        self._paused = False

    def waitting(self):
        return not self._started

    def started(self):
        return self._started and not self._ended

    def running(self):
        return self.started() and not self._paused

    def paused(self):
        return self.started() and self._paused
    
    def ended(self):
        return self._ended

    def start(self):
        if not self.waitting():
            raise ValueError("Game has already started")
        self._started = True

    def pause(self):
        if not self.running():
            raise ValueError("Game is not in progress")
        
        self._paused = True

    def resume(self):
        if not self.paused():
            raise ValueError("Game is not paused")
        self._paused = False

    def end(self):
        if self.ended():
            raise ValueError("Game is ended")
        self._ended = True


class GameServer:
    
    max_n_players: int = 2
    frequency: int = 10
    
    def __init__(self, room_id):
        self.life = GameState()
        self.environment: GameEnvironment = TerritoryTile(
            max_frames=self.frequency * 60 * 6
        )

        self.room_id = room_id
        self.game_id = None

        self.states:  list = []
        self.actions: list = []
        self.players: list = []
        self.recent_action = {}
        self.timer_task = None
        
    @property
    def group_name(self):
        return self.room_id

    def empty(self):
        return len(self.players) == 0

    def full(self):
        return len(self.players) == self.max_n_players
    
    @database_sync_to_async
    def save_frame_action(self, player_id: int, action_dict: dict = None):
        if not action_dict:
            action_dict = self.environment.action_dict(player_id)
        frame = action_dict.get("frame")
        action = action_dict.get("action")
        FrameAction.objects.create(frame=frame, action=action, player_id=player_id)

    @database_sync_to_async
    def save_frame_state(self, state_dict: dict = None):
        if not state_dict:
            state_dict = self.environment.state_dict()
        frame = state_dict.get("frame")
        state = state_dict.get("state")
        FrameState.objects.create(frame=frame, state=state, game_id=self.game_id)
    
    @database_sync_to_async
    def db_create_player(self, strategy_id):
        strategy = Strategy.objects.get(id=strategy_id)
        player_id = Player.objects.create(
            game_id=self.game_id, strategy=strategy
        ).id
        return player_id
    
    async def create_player(self, strategy_id):
        if self.full():
            return None

        if self.life.waitting():
            player_id = await self.db_create_player(strategy_id)
            self.players.append(player_id)
            
            await self.broadcast_game()
            return player_id
        else:
            raise ValueError("Cannot add a player once the game has started.")

    @database_sync_to_async
    def db_destroy_player(self, player_id):
        Player.objects.get(id=player_id).delete()
    
    async def destroy_player(self, player_id):
        if player_id in self.players:
            if self.life.waitting():
                await self.db_destroy_player(player_id)
                self.players.remove(player_id)
            elif self.life.started():
                self.end()
                self.players.remove(player_id)
            elif self.life.ended():
                self.players.remove(player_id)
            else:
                raise ValueError("Game started or cannot found the player_id")
            await self.broadcast_game()

        if self.empty():
            pass
            # TODO

    async def game_timer(self):
        print("------------------ start")
        
        await self.broadcast("signal", "start")
        
        while self.life.started():
            if self.life.running():
                await asyncio.gather(
                    self.broadcast_game_state(take_action=True),
                    asyncio.sleep(1 / self.frequency),
                )
            else:
                await asyncio.sleep(1 / self.frequency)

        print("------------------ end")

    def start(self):
        if self.life.waitting():
            self.life.start()
            self.timer_task = asyncio.create_task(self.game_timer())

    def end(self):
        if self.life.started():
            self.life.end()

    async def signal(self, player_id, content):
        method_name = content
        if hasattr(self.environment, method_name):
            print(f"{method_name}")
            getattr(self.environment, method_name)(player_id)
            
        await self.broadcast_game_state()
        
        print(self.environment.ready())
        
        if method_name == "join" and not self.life.started() and self.environment.ready():
            self.start()
    
    def update(self, content):
        pass

    def player_action(self, player_id, action):
        self.recent_action[player_id] = action
    
    def collect_action(self):
        actions = self.recent_action.copy()
        self.recent_action.clear()
        self.actions.append(actions)
        return actions

    @database_sync_to_async
    def db_get_game_serialized(self):
        game = Game.objects.get(id=self.game_id)
        game_state = GameSerializer(game).data
        return game_state

    async def broadcast_game(self):
        game_state = await self.db_get_game_serialized()
        game_state["latest_framestate"] = self.environment.state_dict()
        self.broadcast("sync.game", game_state)
    
    async def broadcast_game_action(self):
        game_action = self.collect_action()
        try:
            self.environment.step(game_action)
        except Exception as e:
            print(f"[ENV ERROR] {e}")
        game_action = self.environment.action_dict()
        await self.broadcast("sync.game.action", game_action)

    async def broadcast_game_state(self, take_action=False):
        if take_action:
            game_action = self.collect_action()
            self.environment.step(game_action)
        game_state = self.environment.state_dict()
        await self.broadcast("sync.game.state", game_state)

    async def broadcast(self, type, content):
        await get_channel_layer().group_send(
            self.room_id, {"type": type, "content": content}
        )

class GameServerFactory(object):

    @staticmethod
    @database_sync_to_async
    def db_create_game():
        game = Game.objects.create()
        return game.id

    @classmethod
    async def create(cls, room_id: int) -> GameServer:
        
        game_server = GameServer(room_id)
        game_server.game_id = await cls.db_create_game()
        await game_server.save_frame_state()
        
        return game_server

    @classmethod
    async def destroy(cls, instance: GameServer):
        pass


class GameServerRegistry(object):
    _instances = {}

    @classmethod
    async def register(cls, room_id):
        if room_id not in cls._instances.keys():
            print(f"create game server {room_id}")
            cls._instances[room_id] = {
                "instance": await GameServerFactory.create(room_id),
                "counter": 0,
            }
        cls._instances[room_id]["counter"] += 1
        return cls._instances[room_id]["instance"]

    @classmethod
    def available(cls, room_id):
        return room_id not in cls._instances.keys()

    @classmethod
    async def unregister(cls, room_id):
        if room_id not in cls._instances.keys():
            return

        cls._instances[room_id]["counter"] -= 1
        if cls._instances[room_id]["counter"] == 0:
            await GameServerFactory.destroy(
                cls._instances[room_id]["instance"],
            )
            cls._instances.pop(room_id)
            print(f"destroy game server {room_id}")
