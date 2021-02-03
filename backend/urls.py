from django.urls import path

from django.contrib.auth.decorators import permission_required
from django.views.generic.list import ListView

from .models import Service
from .views import ServiceDual

app_name = 'backend'

urlpatterns = [
    path('<str:pk>/', ServiceDual.as_view(), name='service-detail'),
    path('', permission_required('backend.view_service')(ListView.as_view( model = Service )), name='service-list'),
]
