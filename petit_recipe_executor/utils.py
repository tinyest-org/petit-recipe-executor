
import functools
import time

from .datastruct import Recipe


# @time_me
def load_recipe(d: dict) -> Recipe:
    """Reads a dict and returns a valid Recipe"""
    return Recipe(**d)



