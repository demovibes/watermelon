#!/usr/bin/env python
"""
Background script that re-encodes files to the desired .ogg format.

Paired with ices-ogg-only.py, this enables a trade-off of redundant CPU
encode cycles for additional storage space used.  All uploaded files first
go to the MEDIA path, then this script will loop and pick out an uncached
file, transcoding it to the MEDIA/cache/ folder by database ID.
"""

# The order of imports is IMPORTANT!  Django cannot be started without
#  a DJANGO_SETTINGS_MODULE, and the other imports are no good until
#  django.setup() is called.
import sys
from os import environ, nice
from os.path import isfile
from pathlib import Path
from time import sleep

import daemon
import daemon.pidfile

import sox

sys.path.append('/home/pi/src/watermelon')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'demovibes.settings')

# path set up and settings file chosen: load Django.
import django
django.setup()

# now we can import the other Django-specific items and continue.
from django.conf import settings
from demovibes.songs.models import Song

def transcode():
    nice(20)
    while True:
        # get every song from the DB
        for song in Song.objects.filter(is_active=True):
            # build dest path and check if it exists
            print("Checking song id " + str(song.id))
            dest_dir = '{0}/songs_cache/{1}'.format(settings.MEDIA_ROOT, song.id // 1000)
            dest_file = '{0}/{1}.ogg'.format(dest_dir, song.id)
            if not isfile(dest_file):
                Path(dest_dir).mkdir(mode=0o775, parents=True, exist_ok=True)
                source_file = song.song_file.filepath.path
                print(" . Song not found at " + dest_file + ", transcoding from " + source_file);
                # re-encode the file to .ogg
                tfm = sox.Transformer()
                tfm.build_file(source_file, dest_file)

        sleep(60)

with daemon.DaemonContext(pidfile=daemon.pidfile.PIDLockFile('/var/run/background-transcode.pid')):
    transcode()
