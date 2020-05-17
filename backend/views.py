from traceback import format_exc

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import Form
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from .models import Service


# General index page for a Services request
class ServiceList(PermissionRequiredMixin, ListView):
    permission_required = 'backend.view_service'
    model = Service

# #############################################################################
# Specific page of a Service
#  this is a "dual" view that responds differently by POST or GET
class ServiceDual(View):

    def get(self, request, *args, **kwargs):
        view = ServiceDetail.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ServiceForm.as_view()
        return view(request, *args, **kwargs)

class ServiceDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'backend.view_service'
    model = Service

# #############################################################################
class ServiceForm(PermissionRequiredMixin, SingleObjectMixin, FormView):
    permission_required = 'services.change_service'
    model = Service
    form_class = Form

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    # TODO: This method of form handling is very silly.  Maybe it should use
    #  an actual Form class from Django.
    def form_valid(self, form):
        # step through all commands owned by this service, see if any were submit
        for command in self.object.command_set.all():
            if 'command_{0}'.format(command.pk) in form.data:
                result = command.run
                messages.add_message(self.request,
                  messages.SUCCESS if result[0] == 0 else messages.ERROR,
                  'Command {0} returned [{1}]: {2}'.format(command.name, result[0], result[1]))

        # now try any not-readonly files
        for file in self.object.file_set.filter(readonly=False):
            button_name = 'file_save_{0}'.format(file.pk)
            text_name = 'file_content_{0}'.format(file.pk)
            if button_name in form.data and text_name in form.data:
                try:
                    with open(file.path, 'w') as f:
                        f.write(form.data[text_name])
                    messages.success(self.request, 'Saved {0} file ({1}).'.format(file.name, file.path))
                except:
                    messages.error(self.request, "Failed to save {0} file ({1}): the error was:\n{2}".format(file.name, file.path, format_exc(limit=0)))

        # carry on
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('backend:service-detail', kwargs={'pk': self.object.pk})
