major = 0
minor = 1
patch = 0
dev = False

version = '{major}.{minor}.{patch}{dev}'.format(
    major=major, minor=minor, patch=patch, dev='.dev0' if dev else ''
)
