from django.urls import re_path
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from server import consumers

class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        # Get the token from the query string
        query_string = scope.get('query_string', b'').decode('utf-8')
        token_param = [param.split('=')[1] for param in query_string.split('&') if param.startswith('token=')]
        token = token_param[0] if token_param else None

        if token:
            scope['user'] = await self.get_user_from_token(token)

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, token_key):
        try:
            return Token.objects.get(key=token_key).user
        except Token.DoesNotExist:
            return AnonymousUser()


# need token authentication
websocket_urlpatterns = [
    re_path(
        r"ws/play/(?P<room_id>\w+)/(?P<token>\w+)/$",
        consumers.GameConsumer.as_asgi(),
    ),
    re_path(
        r"ws/play/(?P<room_id>\w+)/$",
        consumers.GameConsumer.as_asgi(),
    ),
]

