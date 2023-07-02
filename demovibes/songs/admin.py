from django.contrib import admin

from .models import Song, SongBase


# Register Song model on the Admin page
@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    # SongBase fields should not be editable: these must be changed via the
    #  normal metadata submission process.
    readonly_fields = list(map(lambda field: field.name, SongBase._meta.get_fields()))
