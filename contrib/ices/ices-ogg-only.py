#!/usr/bin/env python
"""
Script to pass songs to IceS - for ONLY OGG-VORBIS stations

This is a simple callback script that chooses the next song from the playlist,
and if none are waiting, it queues a random unlocked song instead.

Filename is printed to command line for IceS to read.
"""

# The ordor of imports is IMPORTANT!  Django cannot be started without
#  a DJANGO_SETTINGS_MODULE, and the other imports are no good until
#  django.setup() is called.
import sys
from os import environ
from os.path import isfile
import json

sys.path.append('/home/pi/src/watermelon')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'demovibes.settings')

# path set up and settings file chosen: load Django.
import django
django.setup()

# now we can import the other Django-specific items and continue.
from django.conf import settings

from django.urls import reverse
from django.utils.timezone import now

from django.contrib.auth.models import User
from demovibes.playlist.models import Entry
from demovibes.songs.models import Song
from demovibes.events.models import Event
from demovibes.playlist.views import queue_song

# choose next unplayed song from playlist
object = Entry.objects.filter(time_play__isnull=True).order_by('-time_play').first()
if object == None:
    # choose random available song to queue
    song = Song.objects.filter(is_active=True, locked_until__lt=now()).order_by('?').first()
    user = User.objects.get(username='DJRandom')
    # construct a new request instead
    object = queue_song(song=song, user=user)

# Check if a cached file exists first, and use that,
#  otherwise use the file right from the DB
source_file = '{0}/songs_cache/{1}/{2}.ogg'.format(settings.MEDIA_ROOT, object.song.id // 1000, object.song.id)
if not isfile(source_file):
    source_file = object.song.song_file.filepath.path

# mark object as "played" and save
object.time_play = now()
object.save()

# build a JSON fragment out of the new song info
event_info = {
    "name": object.song.name,
    "link": reverse('songs:song-detail', kwargs={'pk':object.song.pk}),
    "username": object.user.username,
    "userlink": reverse('user_profiles:profile-detail', kwargs={'slug':object.user.username}),
    "duration": object.song.song_file.duration.total_seconds(),
    "artists": []
}

# add artists
for artist in object.song.artist.all():
    event_info['artists'].append({'name': artist.name, 'link': reverse('artists:artist-detail', kwargs={'pk': artist.pk}) })

# add event to the Event table
event = Event(audience_type=Event.ALL, event_type="PLAYLIST", event_value=json.dumps(event_info))
event.save()

# pass filename to ices
print(source_file)
