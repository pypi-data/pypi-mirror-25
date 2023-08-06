from toolz import curry, reduce


@curry
def converge(fn, fns):
    """
    Returns a function that when called, passes all args to each in fns,
    whose results act as args for a call to fn,
    whose result is then returned.

    example:
    converge(fn, [fn1, fn2])(1, 2)

    example explained:
    both fn1 & fn2 are called with 1 & 2 as their args
    fn is called with the result of fn1 as it's 1st arg and the result of fn2 as it's 2nd arg
    it returns the result of fn
    """
    return lambda *args: fn(*reduce(lambda r, fn: r + [fn(*args)], fns, []))

def identity(*args):
    """
    Returns it's first argument
    """
    return args[0]

def flip(fn):
    """
    Returns a new function that when called will call the original function with the args reversed
    """
    return lambda *args: fn(*list(reversed(args)))
