# Load initial data for the app

from django.db import migrations

def forwards_func(apps, schema_editor):
    Stream = apps.get_model('streams', 'Stream')
    db_alias = schema_editor.connection.alias
    Stream.objects.using(db_alias).bulk_create([
        Stream(url='http://localhost:8080', format='MP3', bitrate=128, owner='admin', notes='Master Stream'),
    ])

def reverse_func(apps, schema_editor):
    Stream = apps.get_model('streams', 'Stream')
    db_alias = schema_editor.connection.alias
    Stream.objects.using(db_alias).filter(url='http://localhost:8080').delete();

class Migration(migrations.Migration):
    dependencies = [
        ('streams', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
