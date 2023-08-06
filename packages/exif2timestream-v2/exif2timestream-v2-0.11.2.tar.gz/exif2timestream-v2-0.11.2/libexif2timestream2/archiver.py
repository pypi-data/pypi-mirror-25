import os
import tarfile
from functools import wraps


def needs_tar(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.tarfile is None:
            self.open()
        return f(self, *args, **kwargs)
    return wrapper


class Archiver(object):
    def __init__(self, path, append=False):
        self.path = path
        self.tarfile = None
        os.makedirs(os.path.dirname(path), exist_ok=True)

        if not append and os.path.exists(path):
            os.remove(self.path)

    def open(self):
        if self.tarfile is None:
            self.tarfile = tarfile.open(self.path, 'a')
        return self

    @needs_tar
    def __add__(self, path):
        if isinstance(path, bytes):
            path = path.decode("utf-8")
        self.tarfile.add(path)
        return self

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.tarfile.close()
        self.tarfile = None
