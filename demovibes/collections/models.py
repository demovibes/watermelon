from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from demovibes.core.models import AutoCreateModify
from demovibes.artists.models import Artist
from demovibes.songs.models import Song


class CollectionType(models.Model):
    """
    Types of collections.  These are used to categorize on the site.
    Initial migration comes with type "album", though others may be
    added as the site admin wishes.
    """

    id = models.SlugField(max_length=191, primary_key=True,
        help_text='ID of the collection type')
    name = models.CharField(max_length=255,
        help_text='Name of the collection type')
    description = models.TextField(blank=True,
        help_text='Description with more information about this collection type')


    def __str__(self):
        return self.name

    class Meta:
        ordering = [ 'id' ]


class CollectionBase(AutoCreateModify):
    """
    CollectionBase is an abstract class of fields which can be updated by users in
    a meta request.  It is useful to avoid redundancy by allowing the same
    field to appear in both places.
    """

    # These fields can be changed in a meta request
    name = models.CharField(max_length=191, db_index=True,
        help_text='Name of the collection')
    image = models.ImageField(upload_to='collections/', max_length=255, blank=True, null=True,
        help_text='Image associated with this collection')
    description = models.TextField(blank=True,
        help_text='Description of the contents of this collection')

    # foreign keys and other links
    artists = models.ManyToManyField(Artist)
    songs = models.ManyToManyField(Song)

    class Meta:
        abstract = True
        ordering = ['name', 'pk']

    def __str__(self):
        return '%s: %s' % (self.collection_type.name, self.name)

class Collection(CollectionBase):
    """
    A Collection is a generic collection of songs or artists.

    Some examples:
    * An Album is a Collection of songs and an artist (or more)
    * A Label may contain Artists (and/or Songs), etc
    * Use a Collection for Group or "artist collective"
    """

    # collection type
    collection_type = models.ForeignKey(CollectionType, on_delete=models.CASCADE,
        help_text='The general type of this collection')
    is_active = models.BooleanField(default=True,
        help_text='Designates whether this song should be treated as active. Unselect this instead of deleting songs.')


    def get_absolute_url(self):
        return reverse('collections:collection-detail', kwargs={'collection_type': self.collection_type.id, 'pk': self.pk})

class CollectionMeta(CollectionBase):
    """
    Supplemental information about an Collection that can be contributed by a user.
    """

    # main collection model this refers to
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE,
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
        ordering = ['collection', 'time_create']

    #def clean(self):
    #    if self.real_name == self.name:
    #        raise ValidationError('Real Name cannot match Name.', code='invalid')

    def get_absolute_url(self):
        return reverse('collections:collectionmeta-detail', kwargs={'collection_type': self.collection.collection_type.id, 'pk': self.pk})

    def __str__(self):
        return '%d ("%s"), %s at %s' % (self.collection.pk, self.name, self.submitter.username, self.time_create)
