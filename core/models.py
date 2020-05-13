from django.db import models


class Setting(models.Model):
    """
    Site-wide global settings that can be changed at run-time.

    The Setting model is a key-value store that is preloaded (using migrations)
    with options that affect the site display. Settings here are available in
    any template ('settings' dict in template context) and can also be brought
    into other apps using Python's standard ``import`` feature.

    Settings cannot be added nor deleted by any user, even an admin.

    When possible, storing new config in this model is preferred to adding new
    entries to settings.py: it is easier for non-coders to manage via the UI,
    and any changes do not require restarting the application.
    """

    key = models.CharField(max_length=191, primary_key=True, editable=False,
        help_text='Setting name')

    description = models.CharField(max_length=255, editable=False,
        help_text='Setting description')

    value = models.CharField(max_length=255, blank=True,
        help_text='Setting value')

    def __str__(self):
        return "%s: '%s'" % (self.key, self.value)
