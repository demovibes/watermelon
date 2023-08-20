# Put some initial content-types in
from django.db import migrations

collection_types = [
      { 'id': 'artist', 'name': 'Artist', 'description': 'A musician is a person who composes, conducts, or performs music.' },
      { 'id': 'album', 'name': 'Album', 'description': 'An album is a collection of audio recordings issued on compact disc (CD), vinyl, audio tape, or another medium such as digital distribution.' },
    ]

def forwards_func(apps, schema_editor):
    CollectionType = apps.get_model('collections', 'CollectionType')
    db_alias = schema_editor.connection.alias
    for collection_type in collection_types:
        CollectionType.objects.using(db_alias).create(**collection_type)

def reverse_func(apps, schema_editor):
    CollectionType = apps.get_model('collections', 'CollectionType')
    db_alias = schema_editor.connection.alias
    for collection_type in collection_types:
        CollectionType.objects.using(db_alias).get(**collection_type).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('collections', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
