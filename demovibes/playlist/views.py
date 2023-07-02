from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import SingleObjectMixin

from demovibes.songs.models import Song

from .models import Entry


# list view showing playlist
class EntryList(TemplateView):
    template_name = "playlist/entry_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entry_upcoming'] = Entry.objects.filter(time_play__isnull=True).order_by('time_request')
        context['entry_recent'] = Entry.objects.filter(time_play__isnull=False).order_by('-time_request')[:20]
        return context

# Add a Song (by ID) to the playlist
class EntryAdd(PermissionRequiredMixin, SingleObjectMixin, View):
    permission_required = 'playlist.add_entry'
    model = Song

    #def post(self, request, **kwargs):
    def get(self, request, **kwargs):
        song = self.get_object()

        # see if we can actually queue the song now
        if (song.available):
            # set locktime on the song
            # make it 25% of total length of all songs in DB
            duration_sum = Song.objects.filter(is_active=True).aggregate(Sum('duration'))['duration__sum']
            #from pprint import pprint
            #pprint(duration_sum)
            song.locked_until = timezone.now() + duration_sum / 2
            song.save()

            # add to playlist
            entry = Entry(user=request.user, song=song)
            entry.save()

            return HttpResponse(status=204)
        else:
            return HttpResponse(status=409, content='Song {0} locked until {1}'.format(song.pk, song.locked_until))
