from django.urls import path

from .views import EntryAdd, EntryList

app_name = 'playlist'

urlpatterns = [
    path('add/<int:pk>/', EntryAdd.as_view(), name='entry-add'),
    path('', EntryList.as_view(), name='entry-list'),
]
