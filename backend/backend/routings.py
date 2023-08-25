from django.urls import re_path

from server import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/interactions/(?P<room_name>\w+)/$",
        consumers.PlayerActionConsumer.as_asgi(),
    ),
]
