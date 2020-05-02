from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Artist, ArtistMeta

# General index page for a Artist request
class ArtistList(ListView):
    model = Artist
    paginate_by = 100  # if pagination is desired

# Specific page of an Artist
class ArtistDetail(DetailView):
    model = Artist

    # Do not display "inactive" artists to non-staff.
    def get_queryset(self):
        queryset = super(ArtistDetail, self).get_queryset()
        if (self.request.user.is_staff):
            return queryset;
        return queryset.filter(active)

# General index page for Artist Meta request
class ArtistMetaList(PermissionRequiredMixin, ListView):
    permission_required = 'artists.view_artistmeta'
    model = ArtistMeta
    paginate_by = 100  # if pagination is desired

# Specific page of an Artist
class ArtistMetaDetail(PermissionRequiredMixin, ListView):
    permission_required = 'artists.view_artistmeta'
    model = ArtistMeta

# Render a form allowing artist metadata changes
class ArtistUpdate(UpdateView):
    model = Artist

    fields = [ 'name', 'image', 'real_name', 'country_code', 'bio', 'alias_of', ]
