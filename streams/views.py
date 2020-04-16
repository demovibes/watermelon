from django.views.generic.list import ListView

from .models import Stream

class StreamsListView(ListView):
    model = Stream
