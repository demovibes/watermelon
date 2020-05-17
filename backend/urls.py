from django.urls import path

from .views import ServiceDual, ServiceList

app_name = 'backend'

urlpatterns = [
    path('<str:pk>/', ServiceDual.as_view(), name='service-detail'),
    path('', ServiceList.as_view(), name='service-list'),
]
