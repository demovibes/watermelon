from django.urls import path

from .views import (SongDetail, SongList, SongMetaCreate, SongMetaDual,
                    SongMetaList)

app_name = 'songs'

urlpatterns = [
    path('meta/<int:pk>/', SongMetaDual.as_view(), name='songmeta-detail'),
    path('meta/', SongMetaList.as_view(), name='songmeta-list'),
    path('<int:song_id>/edit/', SongMetaCreate.as_view(), name='songmeta-create'),
    path('<int:pk>/', SongDetail.as_view(), name='song-detail'),
    path('', SongList.as_view(), name='song-list'),
]
