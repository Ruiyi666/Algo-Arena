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
        fields = ('frame', 'state')

class GameSerializer(serializers.ModelSerializer):
    latest_framestate = serializers.SerializerMethodField()
    players = PlayerSerializer(many=True)
    
    class Meta:
        model = Game
        fields = ('id', 'created_at', 'updated_at', 'latest_framestate', 'metadata', 'players')

    def get_latest_framestate(self, obj):
        latest_state = FrameState.objects.filter(game=obj).latest('frame')
        return FrameStateSerializer(latest_state).data if latest_state else None