from django.urls import path

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Stream
from .views import Player

app_name = 'player'

urlpatterns = [
    path('stream/<int:pk>/', DetailView.as_view( model=Stream ), name='stream-detail'),
    path('stream/', ListView.as_view( model=Stream ), name='stream-list'),

    path('player/', Player.as_view(), name='player'),
]
