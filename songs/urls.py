from django.urls import path

from django.views.generic.list import ListView

from .models import Song
from .views import (SongDetail, SongMetaCreate, SongMetaDual, SongMetaList)

app_name = 'songs'

urlpatterns = [
    path('meta/<int:pk>/', SongMetaDual.as_view(), name='songmeta-detail'),
    path('meta/', SongMetaList.as_view(), name='songmeta-list'),
    path('<int:song_id>/edit/', SongMetaCreate.as_view(), name='songmeta-create'),
    path('<int:pk>/', SongDetail.as_view(), name='song-detail'),
    path('', ListView.as_view( model=Song ), name='song-list'),
]
