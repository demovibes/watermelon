from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from django.views.generic.list import ListView

from .models import Message


class MessageListView(ListView):
    model = Message
    paginate_by = 100  # if pagination is desired

class MessagePostView(PermissionRequiredMixin, View):
    permission_required = 'chat.add_message'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')
