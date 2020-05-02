import sys
from os import environ

sys.path.append('../..')

import django

environ.setdefault('DJANGO_SETTINGS_MODULE', 'demovibes.settings')
django.setup()

from playlist.models import Entry

object = Entry.objects.filter(time_play__isnull=True).order_by('-id').first()
if object == None:
  from songs.models import Song
  # choose random available song to queue
  song = Song.objects.filter(active=True).order_by('?').first()
  # construct a new request
  object = Entry(song=song.pk, user=user.pk)

source_file = object.song.file_set.first().path

# mark object as "played" and save
from django.utils.timezone import now
object.time_play = now
object.save()

# pass filename to ices
print(source_file)
