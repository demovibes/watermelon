# Load data from initial_data.json

from django.db import migrations
from django.core.management import call_command

def forwards_func(apps, schema_editor):
    Service = apps.get_model('backend', 'Service')
    db_alias = schema_editor.connection.alias
    Service.objects.using(db_alias).bulk_create([
        Service(name='Icecast', description='Icecast Streamer',
            command_status='service icecast status',
            command_start='service icecast start',
            command_stop='service icecast stop',
        ),
    ])

def reverse_func(apps, schema_editor):
    Service = apps.get_model('backend', 'Service')
    db_alias = schema_editor.connection.alias
    Service.objects.using(db_alias).filter(name='Icecast').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('backend', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
