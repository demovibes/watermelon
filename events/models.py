from django.db import models


class Event(models.Model):
    '''
    Event entry in the database.

    other models that want to broadcast to the users will save a new Event object.
    '''
    USER = 1
    SUPERUSER = 16
    STAFF = 32
    AUTHENTICATED = 64
    ALL = 128
    AUDIENCE_CHOICES = (
        (USER, 'User'),
        (SUPERUSER, 'Superusers'),
        (STAFF, 'Staff'),
        (AUTHENTICATED, 'Authenticated Users'),
        (ALL, 'All'),
    )

    audience_type = models.PositiveSmallIntegerField(choices=AUDIENCE_CHOICES,
        help_text='Audience who will receive this message')

    audience_value = models.CharField(max_length = 255, blank = True,
        help_text='Audience-specific marker (e.g. username, groupname)')

    event_type = models.CharField(max_length = 10,
        help_text='Source of event, which determines how clients will parse it')

    event_value = models.TextField(
        help_text='Event payload, JSON format')

    event_time = models.DateTimeField(auto_now_add = True,
        help_text='Time that event was added to the queue')
