from django.urls import re_path

from server import consumers

# need token authentication
websocket_urlpatterns = [
    re_path(
        r"ws/(?P<room_name>\w+)/(?P<token>\w+)/$",
        consumers.PlayerActionConsumer.as_asgi(),
    ),
    re_path(
        r"ws/(?P<room_name>\w+)/$",
        consumers.PlayerActionConsumer.as_asgi(),
    ),
]
