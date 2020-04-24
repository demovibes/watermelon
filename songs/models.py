from django.db import models

class File(models.Model):
    path = models.FileField(upload_to='uploads/%Y/%m/%d/',
        help_text='Local path to file on server')

class Platform(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    active = models.BooleanField(default=True, help_text='Designates whether this platform should be treated as active. Unselect this instead of deleting platforms.')

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=200, db_index=True,
        help_text='Name of song')

    active = models.BooleanField(default=True, help_text='Designates whether this song should be treated as active. Unselect this instead of deleting songs.')

    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    # using quotes to refer to Artist class from another app
    artist = models.ForeignKey('artists.Artist', on_delete=models.PROTECT,
        help_text='Artist(s) who created the song')

    # The uploaded file.
    file = models.ForeignKey(File, on_delete=models.PROTECT,
        help_text='File object associated with this song')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('song-detail-view', kwargs={'pk': self.id})

    def __str__(self):
        return self.name
