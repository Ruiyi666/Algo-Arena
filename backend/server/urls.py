from django.urls import path
from . import views

urlpatterns = [
    path("", views.StrategyList.as_view()),
    path("<int:pk>/", views.StrategyDetail.as_view()),
]
