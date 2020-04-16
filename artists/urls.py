from django.urls import path
from .views import ArtistsDetailView, ArtistsListView

urlpatterns = [
    path('', ArtistsListView.as_view()),
    path('<int:pk>', ArtistsDetailView.as_view()),
]
