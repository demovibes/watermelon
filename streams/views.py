from django.http import JsonResponse

from .models import Stream

def index(request):
    stream_list = Stream.objects.order_by('country_code', '-bitrate')

    # put all stream data into a list of dictionary items
    stream_response = [
    {
      'url': s.url,
      'format': s.format,
      'bitrate': s.bitrate,

      'country_code': s.country_code,
      'owner': s.owner,

      'notes': s.notes,
    } for s in stream_list ]

    return JsonResponse(stream_response, safe=False)
