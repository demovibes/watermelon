from django.urls import path
from .views import ArtistListView, ArtistDetailView

urlpatterns = [
    path('', ArtistListView.as_view(), name='artist-list-view'),
    path('<int:pk>/', ArtistDetailView.as_view(), name='artist-detail-view'),
]
