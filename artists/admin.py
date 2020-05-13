from django.contrib import admin

from .models import Artist, ArtistBase


# Register Artist model on the Admin page
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    # ArtistBase fields should not be editable: these must be changed via the
    #  normal metadata submission process.
    readonly_fields = list(map(lambda field: field.name, ArtistBase._meta.get_fields()))
