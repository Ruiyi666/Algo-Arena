from functools import partial
from asgiref.sync import sync_to_async, async_to_sync
from django.core.cache import cache
from rest_framework.authtoken.models import Token
from channels.layers import get_channel_layer
from urllib.parse import parse_qs
from channels.generic.websocket import (
    AsyncWebsocketConsumer,
    WebsocketConsumer,
    JsonWebsocketConsumer,
    AsyncJsonWebsocketConsumer,
)
from .models import Strategy
from .services import GameServerRegistry, GameServer


class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.on_disconnect = []
        
        try:
            self.user = self.scope["user"]
            if not self.user or not self.user.is_authenticated:
                raise ValueError("Unauthorized user")
            await super().connect()
            
            self.strategy_id = await self._get_or_create_strategy()
            await self._register_to_game_service()
            await self._create_player(self.strategy_id)
        except Exception as e:
            await self.close(code=400)
            raise e
        else:
            await self.send_json({
                "type": "connect",
                "content": {
                    "player_id": self.player_id,
                    "game_id": self.game_service.game_id
                }
            })

    async def _get_or_create_strategy(self):
        try:
            strategy = await sync_to_async(Strategy.objects.get)(
                user_id=self.user.id, is_mannual=True)
        except Strategy.DoesNotExist:
            strategy = await sync_to_async(Strategy.objects.create)(
                user_id=self.user.id, 
                name=f"{self.user.username}-default",
                is_mannual=True,
            )
        return strategy.id

    async def _register_to_game_service(self):
        room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.game_service: GameServer = await GameServerRegistry.register(room_id)
        self.on_disconnect.append(partial(GameServerRegistry.unregister, room_id))
        
        await self.channel_layer.group_add(self.game_service.group_name, self.channel_name)
        self.on_disconnect.append(
            partial(self.channel_layer.group_discard, 
                self.game_service.group_name, self.channel_name)
        )

    async def _create_player(self, strategy_id):
        self.player_id = await self.game_service.create_player(strategy_id)
        if self.player_id is None:
            raise ValueError("Failed to create player")
        self.on_disconnect.append(partial(self.game_service.destroy_player, self.player_id))

    async def disconnect(self, close_code):
        for func in reversed(self.on_disconnect):
            await func()
        await super().disconnect(close_code)

    # Receive message from WebSocket
    async def receive_json(self, event):
        assert "content" in event
        assert "type" in event
        assert event["type"] in [
            "signal",
            "update.game",
            "update.game.action",
            "update.game.state",
        ]
        if event["type"] == "signal":
            await self.game_service.signal(self.player_id, event["content"])
        elif event["type"] == "update.game": 
            self.game_service.update(event["content"])
        elif event["type"] == "update.game.action":
            self.game_service.player_action(self.player_id, event["content"])
        
    async def sync_game_action(self, event):
        assert "content" in event
        assert "type" in event
        assert event["type"] == "sync.game.action"
        
        await self.send_json(event)

    async def sync_game_state(self, event):
        assert "content" in event
        assert "type" in event
        assert event["type"] == "sync.game.state"
        
        await self.send_json(event)

    async def sync_game(self, event):
        assert "content" in event
        assert "type" in event
        assert event["type"] == "sync.game"
        
        await self.send_json(event)
        
    async def signal(self, event):
        assert "content" in event
        assert "type" in event
        assert event["type"] == "signal"
        if event["content"] == 'close':
            await self.close()
        else:
            await self.send_json(event)