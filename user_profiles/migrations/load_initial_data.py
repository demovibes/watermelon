from django.db import migrations


# Defines some initial data to load to the system.
def forwards_func(apps, schema_editor):
    from django.utils import timezone
    from django.contrib.auth.models import User
    User.objects.create_superuser(username='admin',
                             email=None,
                             password='password',
                             last_login=timezone.now())
    User.objects.create_user(username='DJRandom',
                             email=None,
                             last_login=timezone.now())

def reverse_func(apps, schema_editor):
    Service = apps.get_model('auth', 'User')
    db_alias = schema_editor.connection.alias
    Service.objects.using(db_alias).in_bulk(['admin', 'djrandom'], field_name='username').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('user_profiles', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
