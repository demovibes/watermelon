import json
import time
from math import ceil
from sys import maxsize

from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.base import View

from core.models import Setting

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
        # last ID available in the database
        try:
            last_event_id = Event.objects.order_by('-id')[0].id
        except IndexError:
            last_event_id = 0

        # last ID seen by the client (default last_event_id)
        client_id = int(request.GET.get('', last_event_id))
        if client_id > last_event_id:
            # prevent requests beyond the current max
            client_id = last_event_id

        # read event settings and determine how long to loop
        delay = int(Setting.objects.get(key='events_delay').value)
        timeout = int(Setting.objects.get(key='events_timeout').value)

        if timeout > 0:
            loops = ceil(timeout / delay)
        else:
            loops = maxsize

        # compose query for events filter
        query = Q(audience_type=Event.ALL)
        if request.user.is_authenticated:
            query.add(Q(audience_type=Event.AUTHENTICATED), Q.OR)
            query.add(Q(audience_type=Event.USER) & Q(audience_value=request.user.username), Q.OR)
        if request.user.is_staff:
            query.add(Q(audience_type=Event.STAFF), Q.OR)
        if request.user.is_superuser:
            query.add(Q(audience_type=Event.SUPERUSER), Q.OR)

        for i in range(loops):
            # check if any events are available to this audience
            available_events = Event.objects.filter(query, id__gt=client_id).order_by('id')
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

            # wait N seconds
            time.sleep(delay)

        # time ran out so just tell the client what the highest ID we saw was
        return JsonResponse( { 'id': last_event_id, 'events': [] } )
