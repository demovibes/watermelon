from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import migrations

from demovibes.collections.models import Collection


def get_initial_songs():
    # 'artist' table is not available until after this script is loaded,
    #  so we have a function to return the initial data set
    return [
      { 'name': 'UnreaL ][ (Second Reality OST)',
        #'artist': (Artist.objects.get(name='Purple Motion').pk,),
        'release_date': datetime(1993,7,30),
        'info': 'Second Reality (originally titled Unreal ] [ - The 2nd Reality) is an IBM PC compatible demo created by Future Crew. It debuted at the Assembly 1993 demoparty on July 30, 1993, where it was entered into the PC demo competition, and finished in first place with its demonstration of 2D and 3D computer graphics rendering. The demo was released to the public in October 1993. It is considered to be one of the best demos created during the early 1990s on the PC; in 1999 Slashdot voted it one of the "Top 10 Hacks of All Time". Its source code was released in a GitHub repository as public domain software using the Unlicense on the 20th anniversary of the release on 1 August 2013.',
        'song_file': {
          'filepath': 'songs/p/pu/Purple_Motion_-_Second_Reality.ogg',
          'hash': b'\x76\x8b\xad\x48\xf8\x0c\x2d\xc5\x98\xf8\x09\xef\x31\xa2\x48\x1e\x30\x50\x71\x31',
          'file_type': 'vorbis',
          'sample_rate': 44100,
          'channels': 2,
          'duration': timedelta(seconds=365.950408),
          'bit_rate': 185078,
        }
      },
    ]

# Defines some initial data to load to the system.
def forwards_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    SongFile = apps.get_model('songs', 'SongFile')
    Song = apps.get_model('songs', 'Song')
    SongMeta = apps.get_model('songs', 'SongMeta')
    admin_id = User.objects.get(username='admin').pk

    # load the songs
    for initial_song in get_initial_songs():
        # artist is many-to-many: we need to extract that entry
        #artist = initial_song.pop('artist')

        # need the Audio File first
        song_file = initial_song.pop('song_file')
        song_file_object = SongFile(**song_file)
        song_file_object.save(using=db_alias)

        # create the song
        song = Song(song_file=song_file_object, **initial_song)
        song.save(using=db_alias)
        # now we can associate artists with it
        #song.artist.set(artist)

        # create a changed_fields out of the things we're going to set
        changed_fields = 'name release_date info filepath'
        song_meta = SongMeta(song=song, reviewed=True, accepted=True, changed_fields=changed_fields, submitter_id=admin_id, song_file=song_file_object, **initial_song)
        song_meta.save(using=db_alias)
        #song_meta.artist.set(artist)

def reverse_func(apps, schema_editor):
    Song = apps.get_model('songs', 'Song')
    db_alias = schema_editor.connection.alias
    for initial_song in get_initial_songs():
        Song.objects.using(db_alias).get(**initial_song).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('songs', '0001_initial'),
        ('collections', 'load_initial_data'),
        ('user_profiles', 'load_initial_data'),
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
