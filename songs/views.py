from django.http import JsonResponse

from .models import Song

def index(request):
    song_list = Song.objects.order_by('name')

    # put all song data into a list of dictionary items
    song_response = [
    {
      'name': s.name,

      'platform': s.platform_id,

      'artist': s.artist.name,
    } for s in song_list ]

    return JsonResponse(song_response, safe=False)
