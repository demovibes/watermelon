# Load initial data for the app

from django.db import migrations

def forwards_func(apps, schema_editor):
    Stream = apps.get_model('player', 'Stream')
    db_alias = schema_editor.connection.alias
    Stream.objects.using(db_alias).bulk_create([
        Stream(url='http://localhost:8000/audio.ogg', format='MP3', bitrate=128, owner='admin', notes='Master Stream'),
    ])

def reverse_func(apps, schema_editor):
    Stream = apps.get_model('player', 'Stream')
    db_alias = schema_editor.connection.alias
    Stream.objects.using(db_alias).filter(url='http://localhost:8000/audio.ogg').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('player', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
