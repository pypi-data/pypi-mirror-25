from nacl.exceptions import ValueError

from salty.config import encoder, paths, Store

from nacl.utils import random
from nacl.secret import SecretBox

from salty.exceptions import NoValidKeyFound, DefaultKeyNotSet


def _new():
    return encoder.encode(random(SecretBox.KEY_SIZE))


def _box(key):
    assert type(key) is bytes

    return SecretBox(key, encoder=encoder)


def _encrypt(message, key=None):
    assert type(message) is bytes

    if key is None:
        if store.current is None:
            raise DefaultKeyNotSet
        key = bytes(store.current, 'utf8')
        return _box(key).encrypt(message, encoder=encoder)

    return _box(key).encrypt(message, encoder=encoder)


def _decrypt(message, key=None):
    assert type(message) is bytes

    if key is None:
        for k in store.keys:
            dk = bytes(k, 'utf8')
            try:
                return _box(dk).decrypt(message, encoder=encoder)
            except ValueError:
                pass
        raise NoValidKeyFound

    return _box(key).decrypt(message, encoder=encoder)


store = Store(default_key=_new().decode())


# public api
def new():
    return _new()


def add(key):
    store.add_key(bytes(key, 'utf8'), current=True)


def set_current(pos):
    store.set_current(pos)


def add_secret(name, raw):
    msg = _encrypt(bytes(raw, 'utf8'), bytes(store.current, 'utf8'))
    store.add_secret(name, msg)


def get_secret(name):
    msg = store.get_secret(name)
    return _decrypt(bytes(msg, 'utf8'))