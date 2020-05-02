from django.urls import path
from .views import ArtistMetaDetail, ArtistMetaList, ArtistDetail, ArtistList, ArtistUpdate

app_name = 'artists'

urlpatterns = [
    path('meta/<int:pk>/', ArtistMetaDetail.as_view(), name='artist-meta-detail'),
    path('meta/', ArtistMetaList.as_view(), name='artist-meta-list'),
    path('<int:pk>/change/', ArtistUpdate.as_view(), name='artist-update-form'),
    path('<int:pk>/', ArtistDetail.as_view(), name='artist-detail'),
    path('', ArtistList.as_view(), name='artist-list'),
]
