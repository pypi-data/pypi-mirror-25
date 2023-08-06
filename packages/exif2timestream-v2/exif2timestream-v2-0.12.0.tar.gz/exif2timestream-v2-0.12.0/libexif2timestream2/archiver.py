import os
import tarfile
from functools import wraps
from .exif import dt_get
from operator import itemgetter
import tempfile

def needs_tar(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.tarfile is None:
            self.open()
        return f(self, *args, **kwargs)
    return wrapper

def needs_write(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.mode not in ('a', 'w'):
            self.mode = 'a'
        if self.tarfile and self.tarfile.mode not in ('a', 'w'):
            self.tarfile.close()
            self.tarfile = None
        self.open()
        return f(self, *args, **kwargs)
    return wrapper

def needs_extract(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.mode != 'r:':
            self.mode = 'r:'
        if self.tarfile and self.tarfile.mode != 'r:':
            self.tarfile.close()
            self.tarfile = None
        self.open()
        return f(self, *args, **kwargs)
    return wrapper


class Archiver(object):
    def __init__(self, path, mode='r:'):
        self.mode = mode
        self.path = path
        self.tarfile = None
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def open(self):
        if self.tarfile is None:
            self.tarfile = tarfile.open(self.path, self.mode)
        return self

    @needs_write
    def __add__(self, path):
        if isinstance(path, bytes):
            path = path.decode("utf-8")
        self.tarfile.add(path)
        return self

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @needs_tar
    def close(self):
        self.tarfile.close()
        self.tarfile = None

    def _keys(self):
        """
        just used to return the unsorted member names

        :return: map iterator of unsorted member names
        """
        return map(lambda x: x.name, self.tarfile.getmembers())

    @needs_extract
    def datetimes(self):
        return sorted(map(lambda x: dt_get(x.name), self.tarfile.getmembers()))


    @needs_extract
    def items_nocompress(self, by_key=False):
        return sorted([(k, dt_get(k, ignore_exif=True)) for k in self._keys()], key=itemgetter(0 if by_key else 1))



    @needs_extract
    def items(self):
        for member in self.tarfile.getmembers():
            with tempfile.TemporaryDirectory(prefix='e2s_temp') as f:
                self.tarfile.extract(member, path=f)
                yield os.path.join(f, member.name), dt_get(member.name, ignore_exif=True)



