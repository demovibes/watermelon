from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Service

# General index page for a Services request
class ServiceListView(PermissionRequiredMixin, ListView):
    permission_required = 'backend.view_service'
    model = Service
    paginate_by = 100  # if pagination is desired

# Specific page of a Service
class ServiceDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'backend.view_service'
    model = Service

    def get_object(self, queryset=None):
        obj = super(ServiceDetailView, self).get_object(queryset=queryset)

        # call status command on object to get code and message
        (obj.status_code, obj.status_message) = obj.get_status()

        # also copy the related objects into a file list
        obj.file_list = obj.file_set.all()

        return obj

