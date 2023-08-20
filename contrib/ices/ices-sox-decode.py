#!/usr/bin/env python
"""
Script to pass songs to IceS - DECODE Songs to raw PCM with SoX

This script runs in tandem with IceS in "stdinpcm" mode, where it
will decode selected library files to a PCM stream and pipe them
through a named pipe (fifo) or similar.
"""

# The order of imports is IMPORTANT!  Django cannot be started without
#  a DJANGO_SETTINGS_MODULE, and the other imports are no good until
#  django.setup() is called.
import sys
from os import environ
import json

from tempfile import NamedTemporaryFile
import sox

sys.path.append('/home/pi/src/watermelon')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'demovibes.settings')

# path set up and settings file chosen: load Django.
import django
django.setup()

# now we can import the other Django-specific items and continue.
from django.urls import reverse
from django.utils.timezone import now

from django.contrib.auth.models import User
from demovibes.playlist.models import Entry
from demovibes.songs.models import Song
from demovibes.events.models import Event

# choose next unplayed song from playlist
object = Entry.objects.filter(time_play__isnull=True).order_by('-time_play').first()
if object == None:
  # choose random available song to queue
  song = Song.objects.filter(is_active=True).order_by('?').first()
  user = User.objects.get(username='DJRandom')
  # construct a new request instead
  object = Entry(song=song, user=user)

source_file = object.song.song_file.filepath.path

# now for the tricky part
# get a temp file
with NamedTemporaryFile(suffix='.wav', delete=False) as f:
    tempfile = f.name

#  re-encode the file to .wav
tfm = sox.Transformer()
tfm.build_file(source_file, tempfile)

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
for artist in object.song.artists:
    event_info['artists'].append({'name': artist.name, 'link': reverse('collections:collection-detail', kwargs={'collection_type': 'artist', 'pk': artist.pk}) })

# add event to the Event table
event = Event(audience_type=Event.ALL, event_type="PLAYLIST", event_value=json.dumps(event_info))
event.save()

# pass filename to ices
print(tempfile)
