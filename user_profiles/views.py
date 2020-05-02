from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from django.core.exceptions import PermissionDenied

from .models import Profile

# General index page for a Profile request
class ProfileList(ListView):
    model = Profile
    paginate_by = 100

# Specific page of a Profile
class ProfileDetail(DetailView):
    model = Profile
    slug_field = "user__username"

# Allow a user to update their own profile
class ProfileUpdate(UpdateView):
    model = Profile
    slug_field = "user__username"
    fields = ['image', 'bio', 'location', 'birth_date']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        # users may only edit their own profiles
        if obj.user != self.request.user:
            raise PermissionDenied

        return obj
