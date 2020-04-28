from django.contrib import admin

from .models import File,Service

# Define an inline admin descriptor for File model
class FileAdminInline(admin.TabularInline):
    model = File

# Define a Service admin with file inlines
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    inlines = (FileAdminInline,)

