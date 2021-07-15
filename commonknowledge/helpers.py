def safe_to_int(x, default=None):
    try:
        return int(x)
    except:
        return default
