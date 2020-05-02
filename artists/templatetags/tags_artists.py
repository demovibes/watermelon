from django import template
from django.utils.html import format_html
from ..models import Artist

register = template.Library()

@register.inclusion_tag('artists/tags_artist.html')
def artist(artist_id):
    """Renders an Artist for presentation"""
    object = Artist.objects.get(pk=artist_id, active=True)
    return { 'object': object }

@register.inclusion_tag('artists/rows_artist.html')
def artist_row(artist_id):
    """Renders a table row of Artist"""
    object = Artist.objects.get(pk=artist_id, active=True)
    return { 'object': object }
