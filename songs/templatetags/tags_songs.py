from django import template

from ..models import Song

register = template.Library()

@register.inclusion_tag('songs/tag_song.html')
def song(song_id):
    """
    Display a Song ID as a link and CSS class.

    Sample usage:

        {% song [id] %}

    This retrieves the song by ``ID`` and creates a link to their detail page, using the song name as the link text.  The link has a unique class (``song``) so it can be styled separately.
    """
    object = Song.objects.get(pk=song_id, is_active=True)
    return { 'object': object }
