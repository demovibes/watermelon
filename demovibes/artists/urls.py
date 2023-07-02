from django.urls import path

from django.views.generic.list import ListView

from .models import Artist
from .views import (ArtistDetail, ArtistMetaCreate, ArtistMetaDual, ArtistMetaList)

app_name = 'artists'

urlpatterns = [
    path('meta/<int:pk>/', ArtistMetaDual.as_view(), name='artistmeta-detail'),
    path('meta/', ArtistMetaList.as_view(), name='artistmeta-list'),
    path('<int:artist_id>/edit/', ArtistMetaCreate.as_view(), name='artistmeta-create'),
    path('<int:pk>/', ArtistDetail.as_view(), name='artist-detail'),
    path('', ListView.as_view( model=Artist, paginate_by=100 ), name='artist-list'),
]
