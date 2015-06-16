import os
import re
import contextlib
import dbm.gnu
import random
import datetime
import string
import logging

from keyserver.key import PublicKey

LOG = logging.getLogger(__name__)
SPLIT_RE = re.compile(r"\W+")


class NotFound(Exception):
    pass


class MultipleFound(Exception):
    pass


def _step_one_dir_in(path):
    l = os.listdir(path)
    if len(l) == 0:
        raise NotFound()
    if len(l) > 1:
        raise MultipleFound()
    return os.path.join(path, l[0])


class DB:

    def __init__(self, path, **kwargs):
        self.path = path
        self._makedirs("req")

    @contextlib.contextmanager
    def _db(self, mode="cf"):
        db = dbm.gnu.open(self._path("index.gdbm", mode))
        try:
            yield db
        finally:
            db.close()

    def _makedirs(self, *path):
        """Create directory tree relative by self.path."""
        try:
            dst = os.path.join(self.path, *path)
            LOG.debug("Making dir %s" % dst)
            os.makedirs(dst)
        except FileExistsError:
            pass
        return dst

    def _path(self, *path):
        """Get path relative to self.path."""
        return os.path.join(self.path, *path)

    def _req_path(self, secret):
        """Get request path by secret."""
        return self._path("req", secret)

    def _get_key_filename(self, fpr):
        """Get path to key by fingerprint.

        0123 4567 89ab cdef 0123  4567 89ab cdef 1234 5678
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^ ^ ^^^^^^^
                              |            |     | |
                              |            |     | |
          +-------------------+------------+-----+ |
          |    +--------------+------------+-------+
          |    |       +------+------------+
          |_ __|___ ___|____ _|__________________
          12/345678/89abcdef/0123456789abcdef0123

          small id           12345678
          big id     89abcdef12345678

        """
        fpr = fpr.lower()
        dst = [self.path, "keys"]
        dst += [fpr[32:34], fpr[34:40], fpr[24:31], fpr[00:23]]
        return os.path.join(*dst)

    def _get_key_path_by_id(self, i):
        if len(i) == 8:
            path = self._path("keys", i[0:2], i[2:8])
        elif len(i) == 16:
            path = self._path("keys", i[8:10], i[10:16], i[0:8])
        else:
            raise ValueError("Invalid len of key ID (%d)" % len(i))
        return path

    def _update_index(self, key):
        data = " ".join(key.details)
        with self._db as db:
            for word in set(SPLIT_RE.split(data)):
                db.setdefault(word, "")
                db[word] = ",".join(filter(bool, db[word], key.fpr[-8:]))

    def get_key_by_id(self, keyid):
        keyid = hex(int(keyid, 16))[2:].lower()
        path = self._get_key_path_by_id(keyid)
        if len(keyid) == 8:
            path = _step_one_dir_in(path)
        path = _step_one_dir_in(path)
        with open(path, "rb") as fp:
            return PublicKey(fp)

    def add_request(self, key):
        secret = ''.join(random.sample(string.ascii_letters, 16))
        with open(self._req_path(secret), "wb") as fp:
            key.export(fp)
        return secret

    def confirm(self, secret):
        self.cleanup_expired_requests()
        src = self._req_path(secret)
        with open(src, "rb") as fp:
            key = PublicKey(fp)
        self._update_index(key)
        fpr = key.fpr
        filename = self._get_key_filename(fpr)
        self._makedirs(filename.rsplit('/', 1)[0])
        os.rename(src, filename)

    def delete_key(self, fpr):
        pass

    def cleanup_expired_requests(self, seconds=300):
        pass

    def _expire_day(self, year, month, day):
        filename = self._path("expire", year, month, day)
        with open(filename, "r") as fp:
            os.unlink(self._get_key_filename(fp.readline()))
        os.unlink(filename)

    def _expire_month(self, year, month):
        for day in os.listdir(self._path("expire", year, month)):
            if self.today.month > int(month) or self.today.day >= int(day):
                self.expire_day(year, month, day)

    def _expire_year(self, year):
        for month in os.listdir(self._path("expire", year)):
            if self.today.year > int(year) or self.today.month >= int(month):
                self._expire_month(year, month)

    def expire(self):
        self.today = datetime.date.today()
        for year in os.listdir(self._path("expire")):
            if self.today.year >= year:
                self._expire_year(year)

    def search(self, string):
        words = SPLIT_RE.split(string)
        if not words:
            return []
        with self._db(mode="r") as db:
            keyids = set(db[words[0]])
            for word in words[1:]:
                keyids = keyids & db[word]
        for keyid in keyids:
            for key in self.get_key_by_id(keyid):
                yield key
