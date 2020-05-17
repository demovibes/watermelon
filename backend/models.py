import os
import shlex
from subprocess import PIPE, STDOUT, run

from django.db import models
from django.utils.functional import cached_property

class Service(models.Model):
    """
    Backend Service model.

    This app is provided to help make management of the streaming services
    easier.  The idea is to add each service's name, description, config file
    location, and commands to start/stop/check status.  From there, an admin
    can use the existing UI to manage backend services.
    """

    name = models.CharField(max_length=191, primary_key=True,
        help_text='Name of the backend service to manage')

    description = models.CharField(max_length=255, blank=True,
        help_text='Brief description of the service')

    pidfile = models.CharField(max_length=255, blank=True,
        help_text='PID file of process.  If set, $PID will be passed to environment of commands.')

    notes = models.TextField(blank=True,
        help_text='Free-form area for leaving notes to yourself')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('backend:service-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s [%s]' % (self.name, self.description)

class Command(models.Model):
    """
    Defines a command that can be run by / on a service.

    Adding a command to a service will create an additional button in the
    detail view.  Clicking the button triggers the command, returning the
    output to the user.

    The option "autorun" will cause the command to be run automatically
    on the detail page.  Usually this is for "status" type commands, so
    service status can be determined quickly.
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    name = models.CharField(max_length=191,
        help_text='Name of the service command')
    command = models.CharField(max_length=255,
        help_text='The actual command to run')

    autorun = models.BooleanField(default=False,
        help_text="Determines if the command should run automatically when visiting the service detail page.  Note: this overrides Service Change permission!")

    @cached_property
    def run(self):
        env = os.environ.copy()
        if self.service.pidfile:
            env['PIDFILE']=self.service.pidfile
            try:
                with open(self.service.pidfile, 'r') as f:
                    env['PID']=f.read()
            except FileNotFoundError:
                pass

        result = run(shlex.split(self.command), stdout=PIPE, stderr=STDOUT, env=env)
        return (result.returncode, result.stdout.decode())

    class Meta:
        unique_together = [['service', 'name']]

class File(models.Model):
    """
    Defines a file associated with a backend service.

    Files added here will appear on the service detail page, with the contents
    placed in text boxes.  Users with service-change permissions can make
    changes to the files and save them.

    Designate a file as "readonly" to prevent it from being changed.

    Typical uses for this would be adding config files, or log files in
    readonly mode.
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    name = models.CharField(max_length=191,
        help_text='Short name to identify the file')

    path = models.CharField(max_length=255,
        help_text='Path to the file on the server')

    readonly = models.BooleanField(default=False,
        help_text='Prevent this file from being edited')

    @cached_property
    def content(self):
        try:
            with open(self.path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return None

    class Meta:
        unique_together = [['service', 'name']]

