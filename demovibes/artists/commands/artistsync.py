from django.core.management.base import BaseCommand, CommandError

from artists.models import Artist, ArtistBase


class Command(BaseCommand):
    help = 'Replay all accepted ArtistMeta into an Artist object'

    def add_arguments(self, parser):
        parser.add_argument('artist_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        meta_fields = list(map(lambda field: field.name, ArtistBase._meta.get_fields()))

        for artist_id in options['artist_ids']:
            try:
                artist = Artist.objects.get(pk=artist_id)
            except Artist.DoesNotExist:
                raise CommandError('Artist "%s" does not exist' % artist_id)

            self.stdout.write('Synchronizing artist "%s"' % artist_id)

            # set all meta fields to empty
            for field in meta_fields:
                setattr(artist, field, None)

            # get all associated meta and "replay" them
            for artistmeta in artist.artistmeta_set.filter(accepted=True).order_by('time_modify'):
                for field in artistmeta.changed_fields.split():
                    setattr(artist, field, getattr(artistmeta, field))
                self.stdout.write(' . Applied metadata change "%s"' % artistmeta.pk)

            # TODO: this should be wrapped in try block
            artist.save()

            self.stdout.write(self.style.SUCCESS('Successfully synchronized artist "%s"' % artist_id))

