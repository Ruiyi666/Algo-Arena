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
from .services import GameService


class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        params = parse_qs(self.scope["query_string"].decode("utf8"))
        token = params.get("token", [None])[0]

        try:
            token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            await self.close()
            return

        self.user = token.user
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        game_service = GameService.load_from_cache(self.room_id)

        if not game_service:
            game_service = GameService(self.room_id)

        strategy_id = Strategy.objects.get(user=self.user, is_mannual=True)
        self.player_id = game_service.create_player(strategy_id=strategy_id)
        if not self.player_id:
            await self.close()

        await self.channel_layer.group_add(self.room_id, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        game_service = GameService.load_from_cache(self.room_id)
        game_service.destory_player(self.player_id)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive_json(self, content):
        game_service = GameService.load_from_cache(self.room_id)

    async def sync_game_action(self, event):
        content = event["content"]
        await self.send_json(content)

    async def sync_game_state(self, event):
        content = event["content"]
        await self.send_json(content)
