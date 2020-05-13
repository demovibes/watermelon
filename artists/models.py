from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class ArtistBase(models.Model):
    """
    ArtistBase is an abstract class of fields which can be updated by users in
    a meta request.  It is useful to avoid redundancy by allowing the same
    field to appear in both places.
    """

    # These fields can be changed in a meta request
    name = models.CharField(max_length=191, db_index=True,
        help_text='Preferred name the artist performs as')
    image = models.ImageField(upload_to='artists/', max_length=255, blank=True, null=True,
        help_text='Image associated with this artist')
    real_name = models.CharField(max_length=255, blank=True,
        help_text="Artist's real name, if different from their performance name")
    country_code = models.CharField(max_length=2, blank=True,
        help_text='Two-letter country code (<a href="https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2">ISO 3166-1</a>)')
    bio = models.TextField(blank=True,
        help_text='Short biography of the artist')

    # foreign keys and other links
    alias_of = models.ForeignKey('Artist', blank=True, null=True, on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_related",
        help_text="If this artist is a pseudonym of another, enter the primary artist ID here.")

    # bookkeeping
    time_create = models.DateTimeField(auto_now_add=True,
        help_text="Timestamp when this item was created")
    time_modify = models.DateTimeField(auto_now=True,
        help_text="Timestamp when this item was modified")

    class Meta:
        abstract = True
        ordering = ['name', 'pk']

    def __str__(self):
        return '%s (%s) [%s]' % (self.name, self.real_name, self.country_code)

class Artist(ArtistBase):
    """
    An Artist is a band, performer, handle, etc. that creates a song.
    More than one Artist can be attached to a Song, so it is not recommended
    to create "combined" artists (like "Queen and David Bowie") for
    collaborations - instead, create two artists and associate them both.
    """

    # basic state flags for artist entry
    is_active = models.BooleanField(default=True,
        help_text='Designates whether this artist should be treated as active. Unselect this instead of deleting artists.')

    # other things only an Admin can change
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.SET_NULL,
        help_text="User account associated with this artist")

    def get_absolute_url(self):
        return reverse('artists:artist-detail', kwargs={'pk': self.pk})

class ArtistMeta(ArtistBase):
    """
    Supplemental information about an Artist that can be contributed by a user.
    """

    # main artist model this refers to
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE,
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
        ordering = ['artist', 'time_create']

    def clean(self):
        if self.real_name == self.name:
            raise ValidationError('Real Name cannot match Name.', code='invalid')

    def get_absolute_url(self):
        return reverse('artists:artistmeta-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%d ("%s"), %s at %s' % (self.artist.pk, self.name, self.submitter.username, self.time_create)
