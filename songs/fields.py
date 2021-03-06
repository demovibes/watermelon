from datetime import timedelta

from django import forms
from django.db.models import signals
from django.db.models.fields.files import FieldFile, FileDescriptor, FileField

from .audios import AudioFile


class AudioFileDescriptor(FileDescriptor):
    """
    Just like the FileDescriptor, but for AudioFields. The only difference is
    calling scan_tool and assigning the metadata fields, if appropriate.
    """
    def __set__(self, instance, value):
        previous_file = instance.__dict__.get(self.field.name)
        super().__set__(instance, value)

        # To prevent recalculating audio fileinfo when we are instantiating
        # an object from the database, only update fileinfo if the field had
        # a value before this assignment.
        if previous_file is not None:
            self.field.update_fileinfo_fields(instance, force=True)


class AudioFieldFile(AudioFile, FieldFile):
    def delete(self, save=True):
        # Clear the audio fileinfo cache
        if hasattr(self, '_fileinfo_cache'):
            del self._fileinfo_cache
        super().delete(save)


class AudioField(FileField):
    attr_class = AudioFieldFile
    descriptor_class = AudioFileDescriptor
    description = "Audio"

    def __init__(self, verbose_name=None, name=None,
      file_type_field=None, sample_rate_field=None, channels_field=None,
      duration_field=None, bit_rate_field=None, encoding_field=None,
      hash_field=None, **kwargs):
        self.file_type_field = file_type_field
        self.sample_rate_field = sample_rate_field
        self.channels_field = channels_field
        self.duration_field = duration_field
        self.bit_rate_field = bit_rate_field
        self.encoding_field = encoding_field
        self.hash_field = hash_field
        super().__init__(verbose_name, name, **kwargs)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
        ]

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.file_type_field:
            kwargs['file_type_field'] = self.file_type_field
        if self.sample_rate_field:
            kwargs['sample_rate_field'] = self.sample_rate_field
        if self.channels_field:
            kwargs['channels_field'] = self.channels_field
        if self.duration_field:
            kwargs['duration_field'] = self.duration_field
        if self.bit_rate_field:
            kwargs['bit_rate_field'] = self.bit_rate_field
        if self.encoding_field:
            kwargs['encoding_field'] = self.encoding_field
        if self.hash_field:
            kwargs['hash_field'] = self.hash_field
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        # Attach update_fileinfo_fields so that fileinfo fields declared
        # after their corresponding audio field don't stay cleared by
        # Model.__init__, see bug #11196.
        # Only run post-initialization fileinfo update on non-abstract models
        if not cls._meta.abstract:
            signals.post_init.connect(self.update_fileinfo_fields, sender=cls)

    def update_fileinfo_fields(self, instance, force=False, *args, **kwargs):
        """
        Update field's metadata fields, if defined.
        """
        # Nothing to update if the field doesn't have fileinfo fields or if
        # the field is deferred.
        has_fileinfo_fields = self.file_type_field or self.sample_rate_field or self.channels_field or self.duration_field or self.bit_rate_field or self.encoding_field or self.hash_field
        if not has_fileinfo_fields or self.attname not in instance.__dict__:
            return

        # getattr will call the AudioFileDescriptor's __get__ method, which
        # coerces the assigned value into an instance of self.attr_class
        # (AudioFieldFile in this case).
        file = getattr(instance, self.attname)

        # Nothing to update if we have no file and not being forced to update.
        if not file and not force:
            return

        fileinfo_fields_filled = not(
            (self.file_type_field and not getattr(instance, self.file_type_field)) or
            (self.sample_rate_field and not getattr(instance, self.sample_rate_field)) or
            (self.channels_field and not getattr(instance, self.channels_field)) or
            (self.duration_field and not getattr(instance, self.duration_field)) or
            (self.bit_rate_field and not getattr(instance, self.bit_rate_field)) or
            (self.encoding_field and not getattr(instance, self.encoding_field)) or
            (self.hash_field and not getattr(instance, self.hash_field))
        )
        # When both fileinfo fields have values, we are most likely loading
        # data from the database or updating an audio field that already had
        # an audio stored.  In the first case, we don't want to update the
        # fileinfo fields because we are already getting their values from the
        # database.  In the second case, we do want to update the fileinfo
        # fields and will skip this return because force will be True since we
        # were called from AudioFileDescriptor.__set__.
        if fileinfo_fields_filled and not force:
            return

        # file should be an instance of AudioFieldFile or should be None.
        if file:
            file_type = file.file_type
            sample_rate = file.sample_rate
            channels = file.channels
            duration = file.duration
            bit_rate = file.bit_rate
            encoding = file.encoding
            hash = file.hash
        else:
            # No file, so clear fileinfo fields.
            file_type = None
            sample_rate = None
            channels = None
            duration = None
            bit_rate = None
            encoding = None
            hash = None

        # Update the metadata fields.
        if self.file_type_field:
            setattr(instance, self.file_type_field, file_type)
        if self.sample_rate_field:
            setattr(instance, self.sample_rate_field, sample_rate)
        if self.channels_field:
            setattr(instance, self.channels_field, channels)
        if self.duration_field:
            setattr(instance, self.duration_field, timedelta(seconds=duration))
        if self.bit_rate_field:
            setattr(instance, self.bit_rate_field, bit_rate)
        if self.encoding_field:
            setattr(instance, self.encoding_field, encoding)
        if self.hash_field:
            setattr(instance, self.hash_field, hash)

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': forms.FileField,
            **kwargs,
        })
