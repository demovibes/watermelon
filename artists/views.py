from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Artist

# General index page for a Artist request
class ArtistListView(ListView):
    model = Artist
    paginate_by = 100  # if pagination is desired

# Specific page of an Artist
class ArtistDetailView(DetailView):
    model = Artist

    # Do not display "inactive" artists to non-staff.
    def get_queryset(self):
        queryset = super(ArtistDetailView, self).get_queryset()
        if (self.request.user.is_staff):
            return queryset;
        return queryset.filter(active)
