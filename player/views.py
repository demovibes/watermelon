from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView

from .models import Stream

# General index page for a Streams request
class StreamListView(ListView):
    model = Stream

# Specific page of a stream
class StreamDetailView(DetailView):
    model = Stream

# Player page
#  Returns streams filtered by active,
#  and a "selected" id based on URL parameter
#  or randomly chosen otherwise
class PlayerView(TemplateView):
    template_name = "player/player.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # produce the stream list
        context['object_list'] = Stream.objects.filter(active=True)

        # attempt to get the desired ID
        object_selected = self.request.GET.get('id')
        # if there is no provided ID, substitute a random one
        if object_selected is None:
          object_selected = context['object_list'].order_by('?').first().pk
        context['object_selected'] = object_selected
        return context
