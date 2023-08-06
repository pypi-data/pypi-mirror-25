import os

from django.utils._os import safe_join
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.finders import FileSystemFinder

from . import app_settings
from .utils import render


class DotdStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        super(DotdStorage, self).__init__(*args, **kwargs)

    def listdir(self, path):
        dirs, filenames = super(DotdStorage, self).listdir(path)

        suffix = app_settings.DIRECTORY_SUFFIX

        # Add matching directories as filenames...
        filenames.extend(x[:-len(suffix)] for x in dirs if x.endswith(suffix))

        # .. and only then filter them out from directories.
        dirs = [x for x in dirs if not x.endswith(suffix)]

        return dirs, filenames

    def _open(self, path, mode):
        pathd = '%s.d' % self.path(path)

        if not os.path.isdir(pathd):
            return ContentFile(render(self.path(path)))

        filenames = []
        for root, _, files in os.walk(pathd, followlinks=True):
            for filename in [os.path.join(root, x) for x in files]:
                if filename.endswith('~'):
                    continue
                filenames.append(filename)

        return ContentFile(b''.join(render(x) for x in sorted(filenames)))


class DotDFinder(FileSystemFinder):
    def __init__(self, *args, **kwargs):
        super(DotDFinder, self).__init__(*args, **kwargs)

        for root, existing_storage in self.storages.items():
            filesystem_storage = DotdStorage(location=root)
            filesystem_storage.prefix = existing_storage.prefix
            self.storages[root] = filesystem_storage

    def find_location(self, root, path, prefix=None):
        if prefix:
            prefix = '%s%s' % (prefix, os.sep)
            if not path.startswith(prefix):
                return None
            path = path[len(prefix):]

        path = safe_join(root, path)
        if os.path.exists(path) or os.path.isdir('%s.d' % path):
            return path
