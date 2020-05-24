from django import template

from ..models import Artist

register = template.Library()

@register.inclusion_tag('artists/tag_artist.html')
def artist(artist_id):
    """
    Display an Artist ID as a link and CSS class.

    Sample usage:

        {% artist [id] %}

    This retrieves the artist by ``ID`` and creates a link to their detail page, using the artist name as the link text.  The link has a unique class (``artist``) so it can be styled separately.
    """
    object = Artist.objects.get(pk=artist_id, is_active=True)
    return { 'object': object }
