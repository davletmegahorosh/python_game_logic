from django.urls import path
from .views import GameAPIView

urlpatterns = [
    path('play/', GameAPIView.as_view())
]
