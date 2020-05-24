from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import Form, ValidationError
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from .models import Song, SongMeta


# #############################################################################
# General index page for a Song request
class SongList(ListView):
    model = Song
    paginate_by = 100

# Specific page of a Song
class SongDetail(DetailView):
    model = Song

    # Do not display "inactive" songs to non-staff.
    def get_queryset(self):
        queryset = super().get_queryset()
        if (self.request.user.is_staff):
            return queryset
        return queryset.filter(is_active=True)

# #############################################################################
# General index page for Song Meta request
class SongMetaList(PermissionRequiredMixin, ListView):
    permission_required = 'songs.view_songmeta'
    model = SongMeta

    # Display only "active" metadata requests.
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(reviewed=False)

# #############################################################################
# Specific page of a Song Meta
#  this is a "dual" view that responds differently by POST or GET
class SongMetaDual(View):

    def get(self, request, *args, **kwargs):
        view = SongMetaDetail.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = SongMetaForm.as_view()
        return view(request, *args, **kwargs)

class SongMetaDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'songs.view_songmeta'
    model = SongMeta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # fill in the table of "changed fields"
        context['changed_fields'] = []
        changed_field_names = self.object.changed_fields.split()

        for field in changed_field_names:
            if (field == 'artist'):
                #current = ' '.join(self.object.song.artist.all())
                current = "\n".join( list(a.name for a in self.object.song.artist.all()) )
                #new = ' '.join(self.object.artist.all())
                new = "\n".join( list(a.name for a in self.object.artist.all()) )
            else:
                current = getattr(self.object.song, field)
                new = getattr(self.object, field)

            context['changed_fields'].append( {
                'name': field,
                'current': current,
                'new': new,
            } )

        # add a form for approve / reject
        context['form'] = Form()
        return context

# #############################################################################
class SongMetaForm(PermissionRequiredMixin, SingleObjectMixin, FormView):
    permission_required = 'songs.change_songmeta'
    template_name = 'songmeta_detail.html'
    form_class = Form
    model = SongMeta

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


    def form_valid(self, form):
        # switch behavior based on accept or reject
        if 'accept' in form.data:
            # copy all changed fields to the parent song and save
            for field in self.object.changed_fields.split():
                if field == 'artist':
                    self.object.song.artist.set(self.object.artist.all())
                else:
                    setattr(self.object.song, field, getattr(self.object, field))

            # save the parent song
            self.object.song.save()

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
        return reverse('songs:songmeta-list')

# #############################################################################
# Render a form allowing song metadata changes
class SongMetaCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'songs.create_songmeta'
    model = SongMeta

    fields = [ 'name', 'artist', 'release_date', 'info', 'filepath', ]

    # the get and post must retrieve the ARTIST base, not ARTIST META.
    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super().get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        # lookup the base object using the provided pk from kwargs
        song = Song.objects.get(pk=self.kwargs['song_id'])
        for field in self.fields:
            if field == 'artist':
                initial['artist'] = song.artist.all()
            else:
                initial[field] = getattr(song, field)
        return initial

    def form_valid(self, form):
        # Get song ID we are supposed to be editing
        song_id = self.kwargs["song_id"]

        # set this on the form so it has the value attached
        form.instance.song_id = song_id

        # set the submiter to be the current user
        form.instance.submitter = self.request.user

        # set the "changed fields" on this request too
        form.instance.changed_fields = " ".join(form.changed_data)

        # if user doesn't have permission to view the result, send them
        #  back to the Song page instead
        if ( self.request.user.has_perm('songs.view_songmeta') == False ):
            self.success_url = reverse('songs:song-detail', kwargs={'pk': song_id})
        return super().form_valid(form)
