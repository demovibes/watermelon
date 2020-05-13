from django import template

#from django.utils.html import format_html
from ..models import Profile

register = template.Library()

@register.inclusion_tag('user_profiles/tag_user.html')
def user(username):
    """Renders a User for presentation, giving a link to their profile page and a class for icon"""
    object = Profile.objects.get(user__username=username, user__is_active=True)
    if (object == None):
        return { 'username': username, 'type': 'none' }
    elif (object.user.is_superuser):
        return { 'username': object.user.username, 'type': 'superuser' }
    elif (object.user.is_staff):
        return { 'username': object.user.username, 'type': 'staff' }
    return { 'username': object.user.username, 'type': 'default' }

#@register.inclusion_tag('user_profiles/rows_user_profile.html')
#def user_profile_row(user_profile_id):
    #"""Renders a table row of Artist"""
    #object = Artist.objects.get(pk=artist_id, active=True)
    #return { 'object': object }
