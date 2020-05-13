from django.contrib import admin

from .models import Setting


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    # these non-editable fields should be readonly
    readonly_fields = ('key', 'description',)
    # enforce fields order
    fields = ('key', 'description', 'value',)

    # prettify the admin page
    list_display = fields

    # disallow any adds or deletes, the only thing anyone can do is change
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
