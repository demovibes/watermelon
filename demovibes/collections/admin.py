from django.contrib import admin

from .models import CollectionType, Collection, CollectionBase

@admin.register(CollectionType)
class CollectionTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'id': ['name']}

# Register Collection model on the Admin page
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    # CollectionBase fields should not be editable: these must be changed via the
    #  normal metadata submission process.
    readonly_fields = list(map(lambda field: field.name, CollectionBase._meta.get_fields()))
