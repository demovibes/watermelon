from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


def id_bucket_path(instance, filename):
    # files are stored in a bucket of up to 250 entries, keyed by song ID
    #  if you change this function, your new uploads will be all over the place...
    bucket_size=250
    bucket = instance.song.pk // bucket_size
    return 'songs/{0:05d}-{1:05d}/{2:05d}_-_{3:s}'.format(bucket_size*bucket, bucket_size*(bucket+1) - 1, instance.song.pk, filename)

class SongBase(models.Model):
    """
    SongBase is an abstract class of fields which can be updated by users in
    a meta request.  It is useful to avoid redundancy by allowing the same
    field to appear in both places.
    """

    # These fields can be changed in a meta request
    name = models.CharField(max_length=191, db_index=True,
        help_text='Name of song')

    # using quotes to refer to Song class from another app
    artist = models.ManyToManyField('artists.Artist',
        help_text='Artist(s) who created the song')

    # The uploaded file.
    path = models.FileField(upload_to=id_bucket_path,
        help_text='Local path to file on server')

    # Some other info
    release_date = models.DateField(blank=True, null=True,
        help_text="Original release date of the song")
    info = models.TextField(blank=True,
        help_text='Additional information about this song')

    # bookkeeping
    time_create = models.DateTimeField(auto_now_add=True,
        help_text="Timestamp when this item was created")
    time_modify = models.DateTimeField(auto_now=True,
        help_text="Timestamp when this item was modified")

    class Meta:
        abstract = True
        ordering = ['name', 'pk']

    def __str__(self):
        return self.name

class Song(SongBase):
    """
    A Song is a single recording.

    Most data about a Song can be changed via metadata request, even the name
    or the underlying file, which means it's possible to 'transform' one song
    into another. This is not recommended: instead, remove the song (by
    setting is_active to True) and create a new one.
    """

    # basic state flags for song entry
    is_active = models.BooleanField(default=True,
        help_text='Designates whether this song should be treated as active. Unselect this instead of deleting songs.')

    def get_absolute_url(self):
        return reverse('songs:song-detail', kwargs={'pk': self.pk})

class SongMeta(SongBase):
    """
    Supplemental information about a Song that can be contributed by a user.
    """

    # main song model this refers to
    song = models.ForeignKey(Song, on_delete=models.CASCADE,
        help_text='The base model for this meta field')

    # space-separated list of fields changed
    changed_fields = models.TextField(max_length=255, editable=False,
        help_text="Fields changed in this metadata request")

    # moderator action on this entry
    reviewed = models.BooleanField(default=False,
        help_text='Indicates whether the field has been reviewed by a moderator.')
    accepted = models.BooleanField(default=False,
        help_text='Indicates whether the field has been accepted by a moderator.')

    # bookkeeping
    submitter = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
        help_text="User account that submitted the meta entry")

    class Meta:
        ordering = ['song', 'time_create']

    def get_absolute_url(self):
        return reverse('songs:songmeta-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%d ("%s"), %s at %s' % (self.song.pk, self.name, self.submitter.username, self.time_create)
