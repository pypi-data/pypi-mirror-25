import os
from .time import str_to_datetime
from functools import wraps
import random
import string
import glob
import datetime
import shelve
import shutil
from operator import itemgetter
from .exif import dt_get

DEFAULT_EXTENSIONS = ["jpeg", "jpg", "tif", "tiff", "cr2", "raw", "nef", "png", "json"]


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
                 dbpath=None,
                 ignore_exif=False):
        """
        Directory database implementation.
        Recursively stores the paths for all files in the directroy.

        default extensions to match are:
            :py:data: `DEFAULT_EXTENSIONS`

        :param paths: paths to inde
        :param extensions: override the default extensions
        :param dbpath: override the directory database path.
        """
        self.ignore_exif = ignore_exif
        paths = list(paths)
        paths.sort()
        for path in paths:
            if not os.path.exists(path) or not os.path.isdir(path):
                raise FileNotFoundError("Path provided doesn't exist")

        if dbpath is None:
            self.dbpath = ".dirdb-{}-{}".format(os.path.basename(paths[0]),
                                                datetime.datetime.fromtimestamp(os.path.getmtime(paths[0])).isoformat())

        if depth is not None:
            self.dbpath = "{}-{}".format(self.dbpath, depth)
        if ignore_exif:
            self.dbpath = self.dbpath + "-ie"

        self.path = paths
        self.extensions = extensions
        # go through extensions...
        for i, x in enumerate(self.extensions):
            if x.startswith("."):
                continue
            self.extensions[i] = "." + x

        self.db = None
        self.depth = depth

        if len(paths) != 1:
            self.dbpath = ".dirdb-multi_{}".format("".join([random.choice(string.ascii_lowercase) for _ in range(4)]))
        else:
            parentdir = os.path.abspath(os.path.join(paths[0], ".."))
            self.dbpath = os.path.join(parentdir, self.dbpath)
            dbfiles = glob.glob(os.path.join(parentdir, ".dirdb-{}*".format(os.path.basename(paths[0]))))
            if self.dbpath in dbfiles:
                dbfiles.remove(self.dbpath)
            else:
                for dbfile in sorted(dbfiles):
                    shutil.move(dbfile, self.dbpath)
            if len(dbfiles) != 0:
                self.reindex()

    @needs_db
    def reindex(self):
        """
        walk path and recreate the dirdb.
        Essentially resets the everything
        """
        for path in self.path:
            for idx, (root, _, files) in enumerate(os.walk(path, topdown=True)):
                for file in filter(lambda fp: fp.lower().endswith(tuple(self.extensions)), files):
                    v = dt_get(file, ignore_exif=self.ignore_exif)
                    if v:
                        self.db[os.path.join(root, file)] = v
                if self.depth is not None and idx >= self.depth:
                    break

    @needs_db
    def __getitem__(self, key):
        if type(key) is not str:
            raise TypeError("Key is not bytes or string")
        if os.path.exists(key):
            v = dt_get(key, ignore_exif=self.ignore_exif)
            if v:
                self.db[key] = v
            return v
        return str_to_datetime(self.db[key])

    @needs_db
    def __contains__(self, key):
        if type(key) is not str:
            raise TypeError("Key is not bytes or string")
        if os.path.exists(key):
            v = dt_get(key, ignore_exif=self.ignore_exif)
            if v:
                self.db[key] = v
        return key in self.db.keys()

    @needs_db
    def keys(self):
        return sorted(self.db.keys())

    @needs_db
    def values(self):
        return sorted([self[k] for k in self.db.keys()])

    @needs_db
    def items(self, by_key=False):
        return sorted([(k, self[k]) for k in self.db.keys()], key=itemgetter(0 if by_key else 1))

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        if self.db is None:
            self.db = shelve.open(self.dbpath, flag='c')
        if len(self.db.keys()) < 1:
            self.reindex()
        return self

    def close(self):
        self.db.close()
        self.db = None
