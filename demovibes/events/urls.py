from django.urls import path

from .views import EventView

app_name = 'events'

urlpatterns = [
    path('', EventView.as_view(), name='event-view'),
]
