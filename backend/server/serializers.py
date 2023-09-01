from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    Strategy,
    Game,
    Player,
    FrameAction,
    FrameState,
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


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"


class FrameActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameAction
        fields = "__all__"


class FrameStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameState
        fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    actions = FrameActionSerializer(many=True, read_only=True)
    states = FrameStateSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = "__all__"
