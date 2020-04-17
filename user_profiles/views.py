from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Profile

# General index page for a Profile request
class ProfileListView(ListView):
    model = Profile
    paginate_by = 100  # if pagination is desired

# Specific page of a song
class ProfileDetailView(DetailView):
    model = Profile
