from datetime import timedelta

from django import template

from ..models import Song

register = template.Library()

@register.simple_tag
def duration( duration ):
    """
    Display a TimeDelta object (or DurationField) as MM:SS.
    """
    if duration:
        if isinstance( duration, timedelta ):
            seconds = round(duration.total_seconds())
            return "{:d}:{:02d}".format( seconds // 60, seconds % 60 )
    # just give up and pass back the value
    return duration

@register.inclusion_tag('songs/tag_song.html')
def song(song_id):
    """
    Display a Song ID as a link and CSS class.

    Sample usage:

        {% song [id] %}

    This retrieves the song by ``ID`` and creates a link to their detail page, using the song name as the link text.  The link has a unique class (``song``) so it can be styled separately.
    """
    if song_id:
        try:
            object = Song.objects.get(pk=song_id, is_active=True)
            return { 'song_id': object.pk, 'name': object.name, }
        except Song.DoesNotExist:
            return { 'name': song_id, }
