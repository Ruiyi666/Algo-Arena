from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    Strategy,
    Game,
    GamePlayer,
    FrameAction,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}


class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = "__all__"


class GamePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamePlayer
        fields = "__all__"


class FrameActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameAction
        fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
    players = GamePlayerSerializer(many=True, read_only=True)
    actions = FrameActionSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = "__all__"
