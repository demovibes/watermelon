from django.urls import path
from .views import EntryListView

urlpatterns = [
    path('', EntryListView.as_view(), name='entry-list-view'),
]
