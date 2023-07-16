from django import template

from ..models import Collection

register = template.Library()

@register.inclusion_tag('collections/tag_collection.html')
def collection(collection_id):
    """
    Display an Collection ID as a link and CSS class.

    Sample usage:

        {% collection [id] %}

    This retrieves the collection ``type`` by ``ID`` and creates a link to the detail page.  The link has a unique class (``collection.type``) so it can be styled separately.
    """
    object = Collection.objects.get(pk=collection_id, is_active=True)
    return { 'object': object }
