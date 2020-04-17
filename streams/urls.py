from django.urls import path
from .views import StreamListView

urlpatterns = [
    path('', StreamListView.as_view()),
]
