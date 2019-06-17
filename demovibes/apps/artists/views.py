from django.http import JsonResponse

from .models import Artist

def index(request):
    return JsonResponse(
        list(Artist.objects.values('id','name','real_name','country_code')),
        safe=False)

# Specific page of an artist
def detail(request, artist_id):
    obj = Artist.objects.get(pk=artist_id)
    return JsonResponse(
        {
            'id': obj.id,
            'name': obj.name,
            'real_name': obj.real_name,
            'country_code': obj.country_code,
            'bio': obj.bio,
        },
        safe=False)
