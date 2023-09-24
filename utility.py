from hashlib import md5


def hash_iterable(iterable):
    # Can Hash list & tuple
    return md5(str(iterable).encode('utf-8')).hexdigest()
