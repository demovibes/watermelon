from django.urls import path
from .views import SongsDetailView, SongsListView

urlpatterns = [
    path('', SongsListView.as_view()),
    path('<int:pk>', SongsDetailView.as_view()),
]
