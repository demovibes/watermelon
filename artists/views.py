from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Artist

# General index page for a Artist request
class ArtistListView(ListView):
    model = Artist
    paginate_by = 100  # if pagination is desired

# Specific page of a song
class ArtistDetailView(DetailView):
    model = Artist
