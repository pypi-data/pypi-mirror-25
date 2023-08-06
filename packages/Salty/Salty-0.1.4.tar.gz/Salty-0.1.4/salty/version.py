# semver
MAJOR = 0
MINOR = 1
PATCH = 4
RELEASE_CANDIDATE = None


__version__ = '%d.%d.%d%s' % (
    MAJOR, MINOR, PATCH,
    '-rc.%d' % RELEASE_CANDIDATE if RELEASE_CANDIDATE is not None else ''
)