import importlib
import hashlib
import os
import sys
from tempfile import NamedTemporaryFile

from django.core.files import File

# This is based off the ImageFile class in Django core.

class AudioFile(File):
    """
    A mixin for use alongside django.core.files.base.File, which provides
    additional features for dealing with audios.
    """
    @property
    def hash(self):
        return self._get_audio_fileinfo().get('hash')
    @property
    def file_type(self):
        return self._get_audio_fileinfo().get('file_type')
    @property
    def sample_rate(self):
        return self._get_audio_fileinfo().get('sample_rate')
    @property
    def channels(self):
        return self._get_audio_fileinfo().get('channels')
    @property
    def duration(self):
        return self._get_audio_fileinfo().get('duration')
    @property
    def bit_rate(self):
        return self._get_audio_fileinfo().get('bit_rate')
    @property
    def encoding(self):
        return self._get_audio_fileinfo().get('encoding')

    def _get_audio_fileinfo(self):
        if not hasattr(self, '_fileinfo_cache'):
            if self.path and os.path.exists(self.path):
                self._fileinfo_cache = get_audio_fileinfo(self.path)
            elif not self.closed:
                # we don't have a filepath BUT we have an open file,
                #  can simply dump it to tempfile
                # save the current file pos
                file_pos = self.tell()
                self.seek(0)
                _, file_extension = os.path.splitext(self.name)
                with NamedTemporaryFile(suffix=file_extension) as temp:
                    temp.write(self.read())
                    self._fileinfo_cache = get_audio_fileinfo(temp.name)
                self.seek(file_pos)
            else:
                raise ValueError("The file cannot be reopened.")
        return self._fileinfo_cache

def get_audio_fileinfo(path):
    """
    Return the (fileinfo) of an audio, given an open file or a path.  Set
    'close' to True to close the file at the end if it is initially in an open
    state.
    """
    from core.models import Setting

    spec = importlib.util.spec_from_file_location('scan_tool', Setting.objects.get(key='scan_tool').value)
    scan_tool = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = scan_tool
    spec.loader.exec_module(scan_tool)

    try:
        ret = scan_tool.scan(path)
    except Exception as e:
        raise ValueError("Failed to parse uploaded file: %s" % str(e))

    # also calculate the hash
    with open(path, 'rb') as f:
        ret['hash'] = hashlib.sha1(f.read()).digest()

    return ret
