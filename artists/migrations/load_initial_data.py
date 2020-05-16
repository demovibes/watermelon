from django.contrib.auth.models import User
from django.core.management import call_command
from django.db import migrations


def get_initial_artists():
    # 'user' table is not available until after this script is loaded,
    #  so we have a function to return the initial data set
    return [
      { 'name': 'DJRandom', 'user_id': User.objects.get(username='DJRandom').pk },
      { 'name': 'Purple Motion', 'real_name': 'Jonne Valtonen', 'country_code': 'fi', 'image': 'artists/Purple_Motion.jpg', 'bio': "Jonne Valtonen (born 23 March 1976) is a Finnish composer, arranger and orchestrator. He is renowned for his contributions in the field of demoscene and tracker music, under the name Purple Motion, and with Future Crew.\r\n\r\nJonne Valtonen was born on 23 March 1976 in Turku, Finland and was raised in Kaarina along with his brother. He began learning to play classical piano at the age of nine.\r\n\r\nValtonen's first music compositions were done on his home computer, a Commodore 64. During his teen years, he became involved in the PC demoscene where he was able to pursue his passion for electronic music production. He has won several awards in this field. Between 1991 and 1996 Valtonen created music for one of the most widely popular groups in the demoscene at the time, the Future Crew. Eventually he became their lead composer under the pseudonym Purple Motion. Some of his best-known compositions are UnreaL ][ / PM (from Future Crew demo Second Reality), Satellite One, and Starshine." },
    ]

# Defines some initial data to load to the system.
def forwards_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    Artist = apps.get_model('artists', 'Artist')
    ArtistMeta = apps.get_model('artists', 'ArtistMeta')
    admin_id = User.objects.get(username='admin').pk

    # load the artists
    for initial_artist in get_initial_artists():
        artist = Artist(**initial_artist)
        artist.save(using=db_alias)
        # artistmeta does not have a 'user_id' field
        try:
            del initial_artist['user_id']
        except KeyError:
            pass

        # create a changed_fields out of the things we're going to set
        changed_fields = ' '.join(initial_artist)
        artistmeta = ArtistMeta(artist=artist, reviewed=True, accepted=True, changed_fields=changed_fields, submitter_id=admin_id, **initial_artist)
        artistmeta.save(using=db_alias)

def reverse_func(apps, schema_editor):
    Artist = apps.get_model('artists', 'Artist')
    db_alias = schema_editor.connection.alias
    for initial_artist in get_initial_artists():
        Artist.objects.using(db_alias).get(**initial_artist).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('artists', '0001_initial'),
        ('user_profiles', 'load_initial_data'),
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
