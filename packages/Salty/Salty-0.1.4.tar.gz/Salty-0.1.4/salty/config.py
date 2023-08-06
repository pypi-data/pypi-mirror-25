import json
from os.path import expanduser, join
from pathlib import Path

import nacl.encoding

__all__ = ['encoder', 'paths', 'Store', 'store']


encoder = nacl.encoding.URLSafeBase64Encoder()

paths = type('paths', (), {})
paths.home = expanduser("~")
paths.config = join(join(paths.home, '.config'), 'salty')
paths.data = join(paths.config, 'data.json')

path = Path(paths.config)
if not path.exists():
    path.mkdir(parents=True)

path = Path(paths.data)
if not path.exists():
    with path.open('w') as fp:
        fp.write('{}')


class Store(object):

    CURRENT = 'current'
    KEYS = 'keys'
    SECRETS = 'secrets'

    _file = None
    _data = None

    def __init__(self, default_key=None):
        assert type(default_key) is str
        self._file = Path(paths.data)
        with self._file.open('r+') as fp:
            self._data = json.load(fp)
        if self.KEYS not in self._data:
            self._data[self.KEYS] = [default_key] if default_key is not None else []
        if self.CURRENT not in self._data:
            self._data[self.CURRENT] = default_key
        if self.SECRETS not in self._data:
            self._data[self.SECRETS] = {}

    @property
    def current(self):
        return self._data[self.CURRENT]

    @property
    def keys(self):
        return self._data[self.KEYS]

    @property
    def secrets(self):
        return self._data[self.SECRETS]

    def add_key(self, key, current=False):
        assert type(key) is bytes

        raw = key.decode()
        if raw not in self._data[self.KEYS]:
            self._data[self.KEYS] += [raw]

        if current:
            self._data[self.CURRENT] = key.decode()

        self.flush()

    def add_secret(self, name, secret):
        assert type(secret is bytes)
        self._data[self.SECRETS][name] = secret.decode()
        self.flush()

    def get_secret(self, name):
        return self._data[self.SECRETS][name]

    def set_current(self, pos):
        if pos > len(self._data[self.KEYS]):
            raise IndexError("Only %d keys found. %d is out of bounds" % (len(self.keys), pos))

        self._data[self.CURRENT] = self._data[self.KEYS][pos]
        self.flush()

    def flush(self):
        with self._file.open('w+') as fp:
            json.dump(self._data, fp)