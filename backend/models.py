from django.db import models

# Backend Service model.
#  This app is provided to help make management of the streaming services
#  easier.  The idea is to add each service's name, description, config file
#  location, and commands to start/stop/check status.  From there, an admin
#  can use the existing UI to manage backend services.

class Service(models.Model):
    name = models.CharField(max_length=200, primary_key=True,
        help_text='Name of the backend service to manage')

    description = models.CharField(max_length=200, blank=True,
        help_text='Brief description of the service')

    command_start = models.CharField(max_length=200, blank=True,
        help_text='System command used to start the service')
    command_stop = models.CharField(max_length=200, blank=True,
        help_text='System command used to stop the service')
    command_status = models.CharField(max_length=200, blank=True,
        help_text='System command used to check the service status')

    notes = models.TextField(blank=True,
        help_text='Free-form area for leaving notes to yourself')

    def get_status(self):
        # Check the status of the running service
        if self.command_status == '':
            return ('N/A', 'Status Command is not configured for this service')
        else:
            from subprocess import run, PIPE, STDOUT
            result = run(self.command_status.split(), stdout=PIPE, stderr=STDOUT)
            return (result.returncode, result.stdout.decode())

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('service-detail-view', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s [%s]' % (self.name, self.description)

class File(models.Model):
    name = models.CharField(max_length=200,
        help_text='Short name to identify the file')

    path = models.CharField(max_length=200,
        help_text='Path to the file on the server')

    readonly = models.BooleanField(
        help_text='Prevent this file from being edited')

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def content(self):
        try:
            with open(self.path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ''

    def __str__(self):
        return self.name
