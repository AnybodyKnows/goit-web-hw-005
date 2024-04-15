from functools import wraps
from time import time


def async_timed(name=None,):
    if name:
        print(name)

    def wrapper(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            start = time()
            result = await func(*args, **kwargs)
            print(f"{func.__name__} took {time()-start} seconds")
            return result
        return wrapped

    return wrapper
