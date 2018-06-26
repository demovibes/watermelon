from django.http import JsonResponse

from .models import Stream

def index(request):
    return JsonResponse(
        list(Stream.objects.values('url','format','bitrate','country_code','owner','notes')),
        safe=False)
