from django.views.generic.list import ListView
from django.views.generic import DetailView

from .models import Song

# General index page for a Songs request
class SongsListView(ListView):
    model = Song
    paginate_by = 100  # if pagination is desired

# Specific page of a song
class SongsDetailView(DetailView):
    model = Song
