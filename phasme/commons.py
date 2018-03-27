
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


def fixed_name(name:str, prefix:str='_c', suffix:str='_', keep_quotes:bool=False) -> str:
    """
    >>> fixed_name('a!-b')
    'a_c33_-b'
    >>> fixed_name('a!-b', prefix='C', suffix='D')
    'aC33D-b'
    >>> fixed_name('"a!b"', keep_quotes=True)
    '"a_c33_b"'
    """
    if keep_quotes:
        if name[0] == '"' and name[-1] == '"':
            name = name[1:-1]
        else:
            keep_quotes = False
    ret = ''.join(c if c.isalnum() or c in '-_'
                  else (prefix + str(ord(c)) + suffix)
                  for c in name)
    return ('"' + ret + '"') if keep_quotes else ret
