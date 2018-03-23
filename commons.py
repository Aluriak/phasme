
import os

edge_predicate = 'edge'


def normalize_filename(fname:str) -> str:
    """Return filename that hopefully is non ambiguous.
    """
    funcs = (
        os.path.expanduser,
        os.path.expandvars,
        os.path.normpath,
        os.path.abspath,
    )
    for func in funcs:
        fname = func(fname)
    return fname
