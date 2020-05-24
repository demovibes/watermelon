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

sys.path.append('/home/grkenn/src/watermelon')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'demovibes.settings')

# path set up and settings file chosen: load Django.
import django
django.setup()

# now we can import the other Django-specific items and continue.
from django.utils.timezone import now
from playlist.models import Entry
from songs.models import Song
from django.contrib.auth.models import User

# choose next unplayed song from playlist
object = Entry.objects.filter(time_play__isnull=True).order_by('-time_play').first()
if object == None:
  # choose random available song to queue
  song = Song.objects.filter(is_active=True).order_by('?').first()
  user = User.objects.get(username='DJRandom')
  # construct a new request instead
  object = Entry(song=song, user=user)

source_file = object.song.filepath.path

# mark object as "played" and save
object.time_play = now()
object.save()

# pass filename to ices
print(source_file)
