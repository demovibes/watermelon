from django.core.management.base import BaseCommand, CommandError

from playlist.models import Entry


class Command(BaseCommand):
    help = 'Removes the top item from the queue, and returns its song ID.  If no requests exist, a random item is queued.'

    def handle(self, *args, **options):
        object = Entry.objects.filter(time_play__isnull=True).order_by('-id').first()
        if object == None:
            from songs.models import Song
            # choose random available song to queue
            song = Song.objects.filter(active=True).order_by('?').first()
            if song == None:
                raise CommandError('No songs are available for random playback.')
            # construct a new request
            object = Entry(song=song.pk, user=user.pk)

        # mark object as "played" and save
        from django.utils.timezone import now
        object.time_play = now
        object.save()

        # return requested song.pk
        return object.song.pk
