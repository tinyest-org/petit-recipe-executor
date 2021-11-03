from .datastruct import Recipe

def load_recipe(d: dict) -> Recipe:
    """Reads a dict and returns a valid Recipe"""
    return Recipe(**d)



