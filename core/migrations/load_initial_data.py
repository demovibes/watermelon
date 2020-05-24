# Load initial data for the app

import os

from django.db import migrations

from demovibes.settings import BASE_DIR

base_settings = [
      { 'key': 'site_name', 'value': 'Watermelon', 'description': 'Site name to display in all pages' },
      { 'key': 'scan_tool', 'value': os.path.join(BASE_DIR, 'contrib/scan/soxi.py'), 'description': 'Path to scan tool, used for getting information about uploaded files' },
    ]

def forwards_func(apps, schema_editor):
    Setting = apps.get_model('core', 'Setting')
    db_alias = schema_editor.connection.alias
    for base_setting in base_settings:
        Setting.objects.using(db_alias).create(**base_setting)

def reverse_func(apps, schema_editor):
    Setting = apps.get_model('core', 'Setting')
    db_alias = schema_editor.connection.alias
    for base_setting in base_settings:
        Setting.objects.using(db_alias).get(**base_setting).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
