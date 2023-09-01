from django.urls import re_path
from server import consumers

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
