def safe_to_int(x, default=None):
    try:
        return int(x)
    except:
        return default


class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)
