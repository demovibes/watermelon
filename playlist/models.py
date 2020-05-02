from django.contrib.auth.models import User
from django.db import models

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey('songs.Song', on_delete=models.CASCADE)

    time_request = models.DateTimeField(auto_now_add=True)
    time_play = models.DateTimeField(null=True)

    objects = models.Manager()

    def __str__(self):
        return self.song
