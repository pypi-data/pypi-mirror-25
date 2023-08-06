import dbm
import os
import time
from functools import wraps
import random
import string

DEFAULT_EXTENSIONS = ["jpeg", "jpg", "tif", "tiff", "cr2", "raw","nef", "png", "json"]

def needs_db(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.db is None:
            self.open()
        return f(self, *args, **kwargs)

    return wrapper

class DirectoryDB(object):
    def __init__(self, paths,
                 extensions=DEFAULT_EXTENSIONS,
                 depth=None,
                 dbpath=None):
        """
        Directory database implementation.
        Recursively stores the paths for all files in the directroy.

        default extensions to match are:
            :py:data: `DEFAULT_EXTENSIONS`

        :param paths: paths to inde
        :param extensions: override the default extensions
        :param dbpath: override the directory database path.
        """
        paths = list(paths)
        paths.sort()
        for path in paths:
            if not os.path.exists(path) or not os.path.isdir(path):
                raise FileNotFoundError("Path provided doesn't exist")

        if dbpath is None:
            self.dbpath = ".dirdb"
        if depth is not None:
            dbpath = "{}-{}".format(dbpath, depth)
            self.dbpath = "{}-{}".format(self.dbpath, depth)

        if len(paths) == 1:
            self.dbpath = dbpath if dbpath is not None else os.path.join(paths[0], self.dbpath)
        else:
            self.dbpath = ".dirdb-multi_{}".format("".join([random.choice(string.ascii_lowercase) for _ in range(4)]))
        # os.makedirs(os.path.dirname(self.dbpath), exist_ok=True)
        # print(os.path.dirname(self.dbpath))
        self.path = paths
        self.extensions = extensions
        # go through extensions...
        for i, x in enumerate(self.extensions):
            if x.startswith("."):
                continue
            self.extensions[i] = "."+x

        self.db = None
        self.depth = depth

    @needs_db
    def reindex(self):
        """
        walk path and recreate the dirdb.
        Essentially resets the everything
        """
        for path in self.path:
            for idx, (root, _, files) in enumerate(os.walk(path, topdown=True)):
                for file in filter(lambda fp: fp.lower().endswith(tuple(self.extensions)), files):
                    self.db[os.path.join(root, file)] = str(time.time())
                if self.depth is not None and idx >= self.depth:
                    break

    @needs_db
    def __getitem__(self, key):
        if type(key) not in (bytes, str):
            raise TypeError("Key is not bytes or string")
        if type(key) is str:
            key = bytes(key, 'utf-8')
        if os.path.exists(key):
            self.db[key] = time.time()
        return self.db[key]

    @needs_db
    def __contains__(self, key):
        if type(key) not in (bytes, str):
            raise TypeError("Key is not bytes or string")
        if type(key) is str:
            key = bytes(key, 'utf-8')
        if os.path.exists(key):
            self.db[key] = time.time()
        return key in self.db.keys()

    @needs_db
    def keys(self):
        return sorted(self.db.keys())

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        if self.db is None:
            self.db = dbm.open(self.dbpath, flag='c')
        if len(self.db.keys()) < 1:
            self.reindex()
        return self

    def close(self):
        self.db.close()
        self.db = None


