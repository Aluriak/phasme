
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


def format_of_file(fname:str) -> str:
    """Return the format used by given file, according to its extension

    >>> format_of_file('test.lp')
    'lp'
    >>> format_of_file('test.gml')
    'gml'

    """
    ext = os.path.splitext(fname)[1].lstrip('.')
    return ext
