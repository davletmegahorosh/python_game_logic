from django.urls import path
from .views import GameWithFileUploadView

urlpatterns = [
    path('play/', GameWithFileUploadView.as_view())
]
