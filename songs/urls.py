from django.urls import path
from .views import SongListView, SongDetailView

urlpatterns = [
    path('', SongListView.as_view(), name='song-list-view'),
    path('<int:pk>/', SongDetailView.as_view(), name='song-detail-view'),
]
