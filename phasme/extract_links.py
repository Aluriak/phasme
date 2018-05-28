
import re
import argparse
import clyngor
from phasme.commons import edge_predicate


def links_from_file(fname:str, edge_predicate:str=edge_predicate):
    """Yield lines read from possibly dirty ASP file. If any error is found,
    a ValueError is raised.
    """
    with open(fname) as fd:
        yield from links_from_lines(fd, edge_predicate=edge_predicate)

def links_from_clean_file(fname:str, edge_predicate:str=edge_predicate):
    """Yield lines read from clean ASP file. If any error is found,
    a ValueError is raised.
    """
    with open(fname) as fd:
        yield from links_from_clean_lines(fd, edge_predicate=edge_predicate)

def links_from_dirty_file(fname:str, edge_predicate:str=edge_predicate):
    """Yield lines read from dirty ASP file. If any error is found,
    a ValueError is raised.
    """
    with open(fname) as fd:
        yield from links_from_dirty_lines(fd, edge_predicate=edge_predicate)


def links_from_lines(lines:iter, edge_predicate:str=edge_predicate):
    """Yield lines read from ASP file. If any error is found,
    the dirty method is used for the remaining lines.
    """
    lines = iter(lines)
    for line in lines:
        try:
            yield from links_from_clean_lines((line,))
        except ValueError:
            yield from links_from_dirty_lines((line,))
            yield from links_from_dirty_lines(lines)

def links_from_clean_lines(lines:str, edge_predicate:str=edge_predicate,
                           handle_comments:bool=True):
    """Yield lines read from clean ASP lines. If any error is found,
    a ValueError is raised.
    """
    field = r'([a-zA-Z0-9_]+|"[^"]*")'
    trailing = '(\s*%.*)?' if handle_comments else ''
    reg = re.compile(str(edge_predicate) + r'\({f},{f}\).{t}'.format(f=field, t=trailing))

    def line_match(line:str) -> tuple or None:
        m = reg.fullmatch(line)
        try:
            return m.groups()[:2]
        except AttributeError:
            raise ValueError("Non compliant ASP data: '{}'".format(line.strip()))

    lines = (line for line in map(str.strip, lines) if line)
    if handle_comments:
        lines = (line for line in lines if not line.startswith('%'))
    yield from map(line_match, lines)


def links_from_dirty_lines(lines:str, edge_predicate:str=edge_predicate):
    """Use the bulldozer to handle these lines by calling ASP solver"""
    models = clyngor.solve(inline=''.join(map(str,lines))).careful_parsing
    for model in models.by_predicate:
        for args in model.get(edge_predicate, ()):
            if len(args) == 2:
                yield args


def read_lines_from_files(fnames:[str]) -> [str]:
    """Yield non-empty lines found in given filename(s)"""
    if isinstance(fnames, str):
        fnames = [fnames]
    for fname in fnames:
        with open(fname) as fd:
            for line in map(str.strip, fd):
                if line: yield line
