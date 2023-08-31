from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from .models import (
    Strategy,
    Game,
    GamePlayer,
    FrameAction,
)
from .serializers import (
    UserSerializer,
    StrategySerializer,
    GameSerializer,
    GamePlayerSerializer,
    FrameActionSerializer,
)

# Create your views here.

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def generate_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return super(UserViewSet, self).get_permissions()

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.save()

        Strategy.objects.create(user=user, name="mannual", is_mannual=True)


class StrategyViewSet(ModelViewSet):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer


class GamePlayerViewSet(ModelViewSet):
    serializer_class = GamePlayerSerializer

    def get_queryset(self):
        game_id = self.kwargs["game_id"]
        return GamePlayer.objects.filter(game__id=game_id)


class FrameActionViewSet(ModelViewSet):
    serializer_class = FrameActionSerializer

    def get_queryset(self):
        game_id = self.kwargs["game_id"]
        return FrameAction.objects.filter(game__id=game_id)


class GameViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
