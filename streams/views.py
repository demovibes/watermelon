from django.views.generic.list import ListView

from .models import Stream

# General index page for a Streams request
class StreamListView(ListView):
    model = Stream
