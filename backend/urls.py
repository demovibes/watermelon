from django.urls import path
from .views import ServiceListView, ServiceDetailView

urlpatterns = [
    path('', ServiceListView.as_view(), name='service-list-view'),
    path('<str:pk>/', ServiceDetailView.as_view(), name='service-detail-view'),
]
