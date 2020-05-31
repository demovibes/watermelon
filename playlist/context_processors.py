from django.utils import timezone

from .models import Entry


def now_playing(request):
    # Retrieves the currently playing song, and returns info about it.
    entry = Entry.objects.filter(time_play__isnull=False).order_by('-time_play').first()
    if entry:
        return {
            'now_playing': entry,
            'now_playing_duration': entry.time_play + entry.song.duration - timezone.now()
        }
    return {}
