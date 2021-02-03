from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import Form, ValidationError
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from .models import Artist, ArtistMeta


# #############################################################################
# Specific page of an Artist
class ArtistDetail(DetailView):
    model = Artist

    # Do not display "inactive" artists to non-staff.
    def get_queryset(self):
        queryset = super().get_queryset()
        if (self.request.user.is_staff):
            return queryset
        return queryset.filter(is_active=True)

# #############################################################################
# General index page for Artist Meta request
class ArtistMetaList(PermissionRequiredMixin, ListView):
    permission_required = 'artists.view_artistmeta'
    model = ArtistMeta

    # Display only "active" metadata requests.
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(reviewed=False)

# #############################################################################
# Specific page of an Artist Meta
#  this is a "dual" view that responds differently by POST or GET
class ArtistMetaDual(View):

    def get(self, request, *args, **kwargs):
        view = ArtistMetaDetail.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ArtistMetaForm.as_view()
        return view(request, *args, **kwargs)

class ArtistMetaDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'artists.view_artistmeta'
    model = ArtistMeta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # fill in the table of "changed fields"
        context['changed_fields'] = []
        changed_field_names = self.object.changed_fields.split()

        for field in changed_field_names:
            context['changed_fields'].append( {
                'name': field,
                'current': getattr(self.object.artist, field),
                'new': getattr(self.object, field)
            } )

        # add a form for approve / reject
        context['form'] = Form()
        return context

# #############################################################################
class ArtistMetaForm(PermissionRequiredMixin, SingleObjectMixin, FormView):
    permission_required = 'artists.change_artistmeta'
    template_name = 'artistmeta_detail.html'
    form_class = Form
    model = ArtistMeta

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # switch behavior based on accept or reject
        if 'accept' in form.data:
            # copy all changed fields to the parent artist and save
            for field in self.object.changed_fields.split():
                setattr(self.object.artist, field, getattr(self.object, field))

            # save the parent artist
            self.object.artist.save()

            # set ourselves as approved
            self.object.accepted = True
        elif 'reject' in form.data:
            self.object.accepted = False
        else:
            raise ValidationError('Invalid POST request', code='invalid')

        # in either case, mark this as reviewed
        self.object.reviewed = True
        self.object.save()

        # carry on
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('artists:artistmeta-list')

# #############################################################################
# Render a form allowing artist metadata changes
class ArtistMetaCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'artists.create_artistmeta'
    model = ArtistMeta

    fields = [ 'name', 'image', 'real_name', 'country_code', 'bio', 'alias_of', ]

    # the get and post must retrieve the ARTIST base, not ARTIST META.
    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super().get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        # lookup the base object using the provided pk from kwargs
        artist = Artist.objects.get(pk=self.kwargs['artist_id'])
        for field in self.fields:
            initial[field] = getattr(artist, field)
        return initial

    def form_valid(self, form):
        # Get artist ID we are supposed to be editing
        artist_id = self.kwargs["artist_id"]

        # set this on the form so it has the value attached
        form.instance.artist_id = artist_id

        # set the submitter to be the current user
        form.instance.submitter = self.request.user

        # set the "changed fields" on this request too
        form.instance.changed_fields = " ".join(form.changed_data)

        # if user doesn't have permission to view the result, send them
        #  back to the Artist page instead
        if ( self.request.user.has_perm('artists.view_artistmeta') == False ):
            self.success_url = reverse('artists:artist-detail', kwargs={'pk': artist_id})
        return super().form_valid(form)
