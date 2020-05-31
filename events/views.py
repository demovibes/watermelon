import json
import time

from django.http import JsonResponse
from django.views.generic.base import View

from .models import Event


class EventView(View):
    '''
    The Event View allows users to "subscribe" to events.
     It optionally accepts a single (anonymous) parameter, the ID of the last
     received event.
    If not specified, the default is the most recent ID.
    It returns a JSON document containing all events visible by the current user.
    If no events are available, it will hold the connection until one arrives.
     This allows JS clients to "long poll" awaiting events.
    The Event table is periodically cleaned when a new event is added
     or retrieved.  Events older than 5 minutes will become unavailable.
    '''
    def get(self, request, *args, **kwargs):
        last_event = Event.objects.last()
        if last_event:
            last_event_id = last_event.id
        else:
            last_event_id = 0

        last_id = request.GET.get('', last_event_id)
        while True:
            # check if any events are available
            available_events = Event.objects.filter(id__gt=last_id).exclude(audience_type=Event.USER, audience_value=request.user.username).order_by('id')
            if available_events:
                response = { 'events': [] }
                for event in available_events:
                    response['id'] = event.id
                    response['events'].append({
                        'id': event.id,
                        'type': event.event_type,
                        'value': json.loads(event.event_value),
                        'timestamp': ( event.event_time.year, event.event_time.month, event.event_time.day, event.event_time.hour, event.event_time.minute, event.event_time.second, event.event_time.microsecond,),
                    })

                return JsonResponse(response)

            # wait 3 seconds
            time.sleep(3)
