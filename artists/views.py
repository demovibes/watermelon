from django.views.generic.list import ListView
from django.views.generic import DetailView

from .models import Artist

# General index page for a Artists request
class ArtistsListView(ListView):
    model = Artist
    paginate_by = 100  # if pagination is desired

# Specific page of a song
class ArtistsDetailView(DetailView):
    model = Artist
