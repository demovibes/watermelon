from django.db import models

class Stream(models.Model):
    url = models.URLField(primary_key=True, max_length=200)
    format = models.CharField(max_length=100, blank=True)
    bitrate = models.PositiveSmallIntegerField(default=0)

    country_code = models.CharField(max_length=2, blank=True)
    owner = models.CharField(max_length=100, blank=True)

    notes = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.url + " [" + self.owner + "'s " + str(self.bitrate) + "kbps " + self.format + " stream]"
