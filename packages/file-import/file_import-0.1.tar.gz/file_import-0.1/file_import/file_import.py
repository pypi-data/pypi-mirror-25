"""
Load a file from a path
"""
from types import SimpleNamespace


def load(path):
    """
    Load a file from path
    """
    result = {}
    with open(path) as f:
        code = compile(f.read(), path, 'exec')
        exec(code, result)

    result = SimpleNamespace(**result)
    return result
