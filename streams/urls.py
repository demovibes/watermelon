from django.urls import path
from .views import StreamsListView

urlpatterns = [
    path('', StreamsListView.as_view()),
]
