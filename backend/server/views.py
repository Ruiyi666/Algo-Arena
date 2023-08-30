from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Strategy, Game
from .serializers import StrategySerializer

# Create your views here.


class StrategyList(generics.ListCreateAPIView):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer


class StrategyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer
