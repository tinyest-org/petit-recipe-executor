
import functools
import time

from .datastruct import Recipe

def time_me(func):
    @functools.wraps(func)
    def f(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} took {end - start} s')
        return res
    return f

# @time_me
def load_recipe(d: dict) -> Recipe:
    """Reads a dict and returns a valid Recipe"""
    return Recipe(**d)



