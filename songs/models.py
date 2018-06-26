from django.db import models

class Platform(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    platform = models.ForeignKey(Platform)

    # using quotes to refer to Artist class from another app
    artist = models.ForeignKey('artists.Artist')

    # The uploaded file.
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')

    def __str__(self):
        return self.name
