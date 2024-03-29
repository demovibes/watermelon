import importlib
import hashlib
import sys
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError

from django.core.files import File
from django.core.files.storage import default_storage
from django.contrib.auth.models import User

from demovibes.collections.models import Collection, CollectionMeta, CollectionType
from demovibes.songs.models import Song, SongMeta, SongFile, upload_to
from demovibes.core.models import Setting

class Command(BaseCommand):
    help = 'Import one or more songs to the system.'

    def add_arguments(self, parser):
        parser.add_argument('paths', nargs='+', type=str)

    def handle(self, *args, **options):
        # import the scan_tool we will use
        spec = importlib.util.spec_from_file_location('scan_tool', Setting.objects.get(key='scan_tool').value)
        scan_tool = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = scan_tool
        spec.loader.exec_module(scan_tool)

        # new artists, songs and metadata are added by "admin"
        admin_id = User.objects.get(username='admin').pk

        # need the collection types for adds
        artist_type = CollectionType.objects.get(id='artist')
        album_type = CollectionType.objects.get(id='album')

        for path in options['paths']:
            # scan the uploaded file
            try:
                info = scan_tool.scan(path)
            except Exception as e:
                raise ValueError("Failed to parse uploaded file: %s" % str(e))

            # also calculate the hash
            with open(path, 'rb') as f:
                filehash = hashlib.sha1(f.read()).digest()

            # construct song meta dict for adding new entries
            file_info = {
                'file_type': info['file_type'],
                'sample_rate': info['sample_rate'],
                'channels': info['channels'],
                'bit_rate': info['bit_rate'],
                'duration': timedelta(seconds=info['duration']),
                'hash': filehash
            }

            song_info = {}
            changed_fields = { 'name', 'filepath' }
            if 'tags' in info:
                if 'title' in info['tags']:
                    song_info['name'] = info['tags']['title']
                    del info['tags']['title']
                else:
                    song_info['name'] = path

                if 'date' in info['tags']:
                    song_info['date'] = datetime.strptime(info['tags']['date'], '%Y-%m-%d')
                    del info['tags']['date']
                    changed_fields.add('release_date')

                if 'artist' in info['tags']:
                    artist_name = info['tags']['artist']
                    del info['tags']['artist']
                    changed_fields.add('collections')


                if 'album' in info['tags']:
                    album_name = info['tags']['album']
                    del info['tags']['album']
                    changed_fields.add('collections')

                if info['tags']:
                    song_info['info'] = "\n".join('{}: {}'.format(key, val) for key, val in info['tags'].items())
                    changed_fields.add('info')

            else:
                song_info['name'] = path
                album_name = None
                artist_name = None

            # get the artist from the DB - if it doesn't exist, we need to create it
            if artist_name:
                try:
                    artist = Collection.objects.get(collection_type=artist_type, name=artist_name)
                except Collection.DoesNotExist:
                    artist = Collection(collection_type=artist_type, name=artist_name)
                    artist.save()

                    artist_meta = CollectionMeta(collection=artist, name=artist_name, changed_fields='name', reviewed=True, accepted=True, submitter_id=admin_id)
                    artist_meta.save()
            else:
                artist = None

            # and the album name
            if album_name:
                try:
                    album = Collection.objects.get(collection_type=album_type, name=album_name)
                except Collection.DoesNotExist:
                    album = Collection(collection_type=album_type, name=album_name)
                    album.save()

                    album_meta = CollectionMeta(collection=album, name=album_name, changed_fields='name', reviewed=True, accepted=True, submitter_id=admin_id)
                    album_meta.save()
            else:
                album = None

            # Everything is parsed.  We're committed to import now!
            #  create the song and meta, and attach the song to it.
            with open(path, 'rb') as f:
                imported_filename = default_storage.save(upload_to(None, path), f)

            # file has been imported to our local filesystem
            #  now we can create an SongFile object around it
            song_file = SongFile(filepath = imported_filename, **file_info)
            song_file.save()

            # add the Song
            song = Song(**song_info)
            song.song_file = song_file
            song.save()

            song_meta = SongMeta(song=song, reviewed=True, accepted=True, changed_fields=' '.join(changed_fields), submitter_id=admin_id, song_file=song_file, **song_info)
            song_meta.save()

            # put song into artist collection
            if artist:
                artist.song_set.add(song)
                artist.save()

            # put both into album collection
            if album:
                album.song_set.add(song)
                if artist:
                    album.related_collections.add(artist)
                album.save()

            self.stdout.write(self.style.SUCCESS('Successfully imported file "%s"' % path))
