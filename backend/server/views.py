from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Strategy, Game
from .serializers import StrategySerializer

# Create your views here.

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def generate_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


class StrategyList(generics.ListCreateAPIView):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer


class StrategyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer
