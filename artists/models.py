from django.db import models

class Artist(models.Model):
    """
    An Artist is a band, performer, handle, etc. that creates a song.
    More than one Artist can be attached to a Song, so it is not recommended
    to create "combined" artists (like "Queen and David Bowie") for
    collaborations - instead, create two artists and associate them both.
    """

    # basic state flags for artist entry
    active = models.BooleanField(default=True,
        help_text='Designates whether this artist should be treated as active. Unselect this instead of deleting artists.')

    # These fields can be changed in a meta request
    name = models.CharField(max_length=191, db_index=True,
        help_text='Preferred name the artist performs as')
    image = models.ImageField(null=True, blank=True,
        help_text='Image associated with this artist')
    real_name = models.CharField(max_length=255, blank=True,
        help_text="Artist's real name, if different from their performance name")
    country_code = models.CharField(max_length=2, blank=True,
        help_text='Two-letter country code (<a href="https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2">ISO 3166-1</a>)')
    bio = models.TextField(blank=True,
        help_text='Short biography of the artist')

    # foreign keys and other links
    user = models.OneToOneField('auth.User', blank=True, null=True, on_delete=models.SET_NULL,
        help_text="User account associated with this artist")
    alias_of = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL,
        help_text="If this artist is a pseudonym of another, enter the primary artist ID here.")

    # bookkeeping
    time_create = models.DateTimeField(auto_now_add=True,
        help_text="Timestamp when this item was created")
    time_modify = models.DateTimeField(auto_now=True,
        help_text="Timestamp when this item was modified")

    class Meta:
        ordering = ['name', 'pk']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('artists:artist-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s (%s) [%s]' % (self.name, self.real_name, self.country_code)

class ArtistMeta(models.Model):
    """
    Supplemental information about an Artist that can be contributed by a user.
    """

    # main artist model this refers to
    base = models.ForeignKey(Artist, on_delete=models.CASCADE,
        help_text='The base model for this meta field')

    # moderator action on this entry
    reviewed = models.BooleanField(default=False,
        help_text='Indicates whether the field has been reviewed by a moderator.')
    #approved = models.BooleanField(default=False,
    #    help_text='Indicates whether the field has been approved by a moderator.')

    # meta fields - same as above
    name = models.CharField(max_length=191,
        help_text='Preferred name the artist performs as')
    image = models.ImageField(null=True, blank=True,
        help_text='Image associated with this artist')
    real_name = models.CharField(max_length=200, blank=True,
        help_text="Artist's real name, if different from their performance name")
    country_code = models.CharField(max_length=2, blank=True,
        help_text='Two-letter country code (<a href="https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2">ISO 3166-1</a>)')
    bio = models.TextField(blank=True,
        help_text='Short biography of the artist')
    alias_of = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL,
        help_text="If this artist is a pseudonym of another, enter the primary artist ID here.")

    # bookkeeping
    submitter = models.ForeignKey('auth.User', null=True, on_delete=models.SET_NULL,
        help_text="User account that submitted the meta entry")
    time_create = models.DateTimeField(auto_now_add=True,
        help_text="Timestamp when this item was created")
    time_modify = models.DateTimeField(auto_now=True,
        help_text="Timestamp when this item was modified")

    class Meta:
        ordering = ['base', 'time_create']

    #def clean(self):
        #"""Validate that name and real_name are different."""
        #if self.real_name == self.name:
            #raise ValidationError('Real Name cannot match Name.', code='invalid')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('artists:artist-meta-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%d ("%s"), %s at %s' % (self.base, self.name, self.submitter.name, self.time_create)
