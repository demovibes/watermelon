from django.urls import path

from .views import Player, StreamDetail, StreamList

app_name = 'player'

urlpatterns = [
    path('stream/<int:pk>/', StreamDetail.as_view(), name='stream-detail'),
    path('stream/', StreamList.as_view(), name='stream-list'),

    path('player/', Player.as_view(), name='player'),
]
