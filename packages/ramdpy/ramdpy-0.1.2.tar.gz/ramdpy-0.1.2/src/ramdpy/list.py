from toolz import curry, reduce

@curry
def append(arr, n):
    """
    Returns a copy of list arg, with item arg appended
    """
    return arr + [n]

def concat(*args):
    """
    Concatenate all args
    """
    return reduce(lambda r, n: r + n, args, [])
