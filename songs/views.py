from django.http import JsonResponse
from django.forms.models import model_to_dict

from .models import Song

# General index page for a Songs request
def index(request):
    return JsonResponse(
        list(Song.objects.values('id','name','platform','artist')),
        safe=False)

# Specific page of a song
def detail(request, song_id):
    obj = Song.objects.get(pk=song_id)
    return JsonResponse(
        {
            'id': obj.id,
            'name': obj.name,
            'platform': obj.platform_id,
            'artist_id': obj.artist_id,
            'artist_name': obj.artist.name,
        },
        safe=False)
