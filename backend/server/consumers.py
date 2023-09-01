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
        params = parse_qs(self.scope["query_string"].decode("utf8"))
        token = params.get("token", [None])[0]

        try:
            token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            await self.close()
            return

        self.user = token.user

        strategy_id = Strategy.objects.get(user=self.user, is_mannual=True)

        self.game_service: GameServer = GameServerRegistry.register(
            self.scope["url_route"]["kwargs"]["room_id"]
        )

        self.player_id = self.game_service.create_player(strategy_id=strategy_id)
        if not self.player_id:
            await self.close()

        # enter the channel
        await self.channel_layer.group_add(
            self.game_service.group_name, self.channel_name
        )
        await super().connect()

    async def disconnect(self, close_code):
        await super().disconnect()

        # leave the channel
        await self.channel_layer.group_discard(
            self.game_service.group_name, self.channel_name
        )
        self.game_service.destory_player(self.player_id)
        GameServerRegistry.unregister(self.scope["url_route"]["kwargs"]["room_id"])

    # Receive message from WebSocket
    async def receive_json(self, content):
        pass

    async def sync_game_action(self, event):
        content = event["content"]
        await self.send_json(content)

    async def sync_game_state(self, event):
        content = event["content"]
        await self.send_json(content)
