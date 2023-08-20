from django.contrib import admin

from .models import Command, File, Service


# Define an inline admin descriptor for File model
class FileAdminInline(admin.TabularInline):
    model = File

# Define an inline admin descriptor for Command model
class CommandAdminInline(admin.TabularInline):
    model = Command

# Define a Service admin with file inlines
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'id': ['name']}
    inlines = (CommandAdminInline, FileAdminInline,)
