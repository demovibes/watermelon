from django.core.exceptions import PermissionDenied
from django.views.generic.edit import UpdateView

from .models import Profile


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
