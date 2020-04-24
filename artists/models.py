from django.db import models

# Artist model.
#  The Artist is a band, performer, handle, etc. that creates a song.
# More than one Artist can be attached to a Song, so it is not recommended
#  to create "combined" artists (like "Queen and David Bowie") for
#  collaborations - instead, create two artists and associate them both.

class Artist(models.Model):
    name = models.CharField(max_length=200, db_index=True,
        help_text='Preferred name the artist performs as')

    active = models.BooleanField(default=True,
        help_text='Designates whether this artist should be treated as active. Unselect this instead of deleting artists.')

    image = models.ImageField(null=True,
        help_text='Image associated with this artist')

    real_name = models.CharField(max_length=200, blank=True,
        help_text="Artist's real name, if different from their performance name")
    country_code = models.CharField(max_length=2, blank=True,
        help_text='Two-letter country code (<a href="https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2">ISO 3166-1</a>)')
    bio = models.TextField(blank=True,
        help_text='Short biography of the artist')

    alias_of = models.OneToOneField('self', blank=True, null=True, on_delete=models.SET_NULL,
        help_text="If this artist is a pseudonym of another, enter the primary artist ID here.")
    user = models.OneToOneField('auth.User', blank=True, null=True, on_delete=models.SET_NULL,
        help_text="User account associated with this artist")

    class Meta:
        ordering = ['name']

    def clean(self):
        if self.real_name == self.name:
            raise ValidationError('Real Name cannot match Name.', code='invalid')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('artist-detail-view', kwargs={'pk': self.id})

    def __str__(self):
        return '%s (%s) [%s]' % (self.name, self.real_name, self.country_code)
