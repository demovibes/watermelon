import json

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.template.defaultfilters import time as TimeFilter

from demovibes.events.models import Event

from .models import Message

class MessagePost(PermissionRequiredMixin, CreateView):
    permission_required = 'chat.add_message'
    model = Message
    fields = [ 'text' ]

    def form_valid(self, form):
        # set the submitter to be the current user
        form.instance.user = self.request.user

        # save the posted message
        self.object = form.save()

        # add event to the Event table
        # build a JSON fragment out of the new song info
        event_info = {
            "user": self.object.user.username,
            "time": TimeFilter(self.object.time),
            "text": self.object.text,
        }
        if self.object.user.is_superuser:
            event_info['user_class'] = "superuser"
        elif self.object.user.is_staff:
            event_info['user_class'] = "staff"
        elif self.object.user.is_active:
            event_info['user_class'] = "default"
        else:
            event_info['user_class'] = "none"

        event = Event(audience_type=Event.AUTHENTICATED, event_type="CHAT", event_value=json.dumps(event_info))
        event.save()

        # return 204 NO CONTENT (prevents redirect)
        return HttpResponse(status=204)
