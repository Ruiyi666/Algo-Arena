from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    StrategyViewSet,
    GameViewSet,
    PlayerViewSet,
    FrameActionViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"strategies", StrategyViewSet)
router.register(r"games", GameViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "games/<int:game_id>/players/",
        PlayerViewSet.as_view({"get": "list", "post": "create"}),
        name="game-players-list",
    ),
    path(
        "games/<int:game_id>/players/<int:pk>/",
        PlayerViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="game-player-detail",
    ),
    path(
        "games/<int:game_id>/actions/",
        FrameActionViewSet.as_view({"get": "list", "post": "create"}),
        name="game-actions-list",
    ),
    path(
        "games/<int:game_id>/actions/<int:pk>/",
        FrameActionViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="game-action-detail",
    ),
]
