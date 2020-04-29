from django.db import models

class Stream(models.Model):
    url = models.URLField(unique=True, max_length=200,
        help_text='URL of the stream')

    active = models.BooleanField(default=True, help_text='Designates whether this stream should be treated as active. Unselect this instead of deleting streams.')

    format = models.CharField(max_length=100, blank=True,
        help_text='Format of stream breadcast (e.g. MP3, OGG, etc)')
    bitrate = models.PositiveSmallIntegerField(default=0,
        help_text='Bitrate of the stream')

    country_code = models.CharField(max_length=2, blank=True,
        help_text='Country code where the stream is located')
    owner = models.CharField(max_length=100, blank=True,
        help_text='Username of the stream owner')

    notes = models.TextField(blank=True,
        help_text='Additional information about the stream')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('streams-detail-view', kwargs={'pk': self.pk})

    def __str__(self):
        return "%s [%s's %dkbps %s stream]" % (self.url, self.owner, self.bitrate, self.format)
