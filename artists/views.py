from django.http import JsonResponse

from .models import Artist

def index(request):
    artist_list = Artist.objects.order_by('name','real_name')

    # put all artist data into a list of dictionary items
    artist_response = [
    {
      'name': a.name,
      'real_name': a.real_name,

      'country_code': a.country_code,

      'bio': a.bio,
    } for a in artist_list ]

    return JsonResponse(artist_response, safe=False)
