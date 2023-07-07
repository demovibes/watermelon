# Load data from initial_data.json

from django.db import migrations


def get_initial_services():
    return [
      { 'name': 'Icecast', 'description': 'Icecast Streamer', 'command': [
          { 'name': 'status', 'command': 'service icecast status', 'autorun': True },
          { 'name': 'start', 'command': 'service icecast start' },
          { 'name': 'stop', 'command': 'service icecast stop' },
        ], 'file': [
          { 'name': 'Service Config', 'path': '/usr/local/etc/icecast.xml', },
          { 'name': 'Access Log', 'path': '/var/log/icecast/access.log', 'readonly': True, },
          { 'name': 'Error Log', 'path': '/var/log/icecast/error.log', 'readonly': True, },
        ]
      },
      { 'name': 'IceS', 'description': 'Icecast source client', 'pidfile': '/var/run/ices.pid', 'command': [
          { 'name': 'status', 'command': 'kill -0 $PID', 'autorun': True },
          { 'name': 'start', 'command': '/usr/local/bin/ices /usr/local/etc/ices.xml', 'background': True },
          { 'name': 'stop', 'command': 'kill -INT $PID' },
          { 'name': 'next', 'command': 'kill -HUP $PID' },
          { 'name': 'sync', 'command': 'kill -USR1 $PID' },
        ], 'file': [
          { 'name': 'Service Config', 'path': '/usr/local/etc/ices.xml', },
          { 'name': 'Output Log', 'path': '/var/log/ices/ices.log', 'readonly': True, },
        ]
      },
      { 'name': 'Background-Transcode', 'description': 'Background transcoding (cache) files to .ogg format', 'pidfile': '/var/run/background-transcode.pid', 'command': [
          { 'name': 'status', 'command': 'kill -0 $PID', 'autorun': True },
          { 'name': 'start', 'command': '/home/pi/src/watermelon/contrib/ices/background-transcode.py' },
          { 'name': 'stop', 'command': 'kill -INT $PID' },
        ], 'file': [ ]
      },
    ]

# Defines some initial data to load to the system.
def forwards_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    Service = apps.get_model('backend', 'Service')
    Command = apps.get_model('backend', 'Command')
    File = apps.get_model('backend', 'File')

    # load the services
    for initial_service in get_initial_services():
        # pop the commands and files for followup insert
        commands = initial_service.pop('command')
        files = initial_service.pop('file')

        # create the service
        service = Service(**initial_service)
        service.save(using=db_alias)

        # add the commands to it
        for service_command in commands:
            # if autorun, we want to link this ID back on the main service.
            try:
                autorun = service_command.pop('autorun')
            except KeyError:
                autorun = False
            command = Command(**service_command)
            command.service = service
            command.save(using=db_alias)
            if autorun:
                service.autorun_command = command
                service.save(using=db_alias)

        for service_file in files:
            file = File(**service_file)
            file.service = service
            file.save(using=db_alias)

def reverse_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    Service = apps.get_model('backend', 'Service')

    for initial_service in get_initial_services():
        Service.objects.using(db_alias).get(**initial_service).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('backend', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
