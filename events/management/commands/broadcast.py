from django.core.management.base import BaseCommand

from events.models import Event


class Command(BaseCommand):
    help = 'Broadcast an Event to all connected clients.'

    def add_arguments(self, parser):
        parser.add_argument('message', type=str)

    def handle(self, *args, **options):
        message = options['message']
        event = Event(audience_type=Event.ALL, audience_value="", event_type='GENERIC', event_value='{ "message": "%s" }' % message)
        event.save()
        self.stdout.write(self.style.SUCCESS('Added new broadcast event, id=%s, message="%s"' % (event.id, message)))
