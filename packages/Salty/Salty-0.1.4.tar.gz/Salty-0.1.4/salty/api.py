import nacl.exceptions
import nacl.utils
import nacl.secret

from salty.config import encoder, Store
from salty.exceptions import NoValidKeyFound, DefaultKeyNotSet


__all__ = ['new', 'current', 'select', 'add_secret', 'get_secret', 'encrypt', 'decrypt']


def _new():
    return encoder.encode(nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE))


def _box(key):
    assert type(key) is bytes

    return nacl.secret.SecretBox(key, encoder=encoder)


def _encrypt(message, key=None):
    assert type(message) is bytes

    if key is None:
        if store.current is None:
            raise DefaultKeyNotSet
        key = bytes(store.current, 'utf8')
        return _box(key).encrypt(message, encoder=encoder)

    return _box(key).encrypt(message, encoder=encoder)


def _decrypt(name, key=None):
    assert type(name) is bytes

    if key is None:
        for k in store.keys:
            dk = bytes(k, 'utf8')
            try:
                return _box(dk).decrypt(name, encoder=encoder)
            except nacl.exceptions.CryptoError:
                continue
        raise NoValidKeyFound

    return _box(key).decrypt(name, encoder=encoder)


store = Store(default_key=_new().decode())


# public api
def new():
    return _new()


def current(key=None):
    if key is None:
        return store.current

    store.add_key(bytes(key, 'utf8'), current=True)

    return True


def select(pos):
    store.set_current(pos)

    return True


def add_secret(name, raw):
    msg = _encrypt(bytes(raw, 'utf8'), bytes(store.current, 'utf8'))
    store.add_secret(name, msg)

    return True


def get_secret(name):
    msg = store.get_secret(name)

    return _decrypt(bytes(msg, 'utf8'))


def secrets():
    return store.secrets


def decrypt(name, key=None):
    key = key or current()

    return _decrypt(name, key)


def encrypt(message, key=None):
    key = key or current()

    return _encrypt(message, key)
