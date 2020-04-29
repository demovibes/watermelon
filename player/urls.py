from django.urls import path
from .views import StreamListView, StreamDetailView, PlayerView

urlpatterns = [
    path('stream/', StreamListView.as_view(), name='stream-list-view'),
    path('stream/<int:pk>/', StreamDetailView.as_view(), name='stream-detail-view'),

    path('player/', PlayerView.as_view(), name='player-view'),
]
