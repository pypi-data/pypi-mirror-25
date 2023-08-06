

class EncryptException(BaseException):
    pass


class DecryptException(BaseException):
    pass


class DefaultKeyNotSet(EncryptException):
    pass


class NoValidKeyFound(DecryptException):
    pass
