

from phasme.commons import edge_predicate

def as_asp_value(smth:object) -> str:
    """Return given value as an ASP-compliant string

    >>> as_asp_value(7)
    '7'
    >>> as_asp_value('a')
    'a'
    >>> as_asp_value('0a')
    '"0a"'
    >>> as_asp_value('A')
    '"A"'
    >>> as_asp_value(',')
    '","'
    >>> as_asp_value('')
    '""'
    >>> as_asp_value('""')
    '""'

    """
    if isinstance(smth, int):
        return str(smth)
    if isinstance(smth, str) and smth.isidentifier() and not smth[0].isupper():
        return smth
    return quoted(str(smth))


def quoted(value:str, by='"'):
    """
    >>> quoted('a')
    '"a"'
    >>> quoted('"i')
    '"i"'
    >>> quoted('"i', by='a')
    'a"ia'
    """
    return (('' if value.startswith(by) else by)
            + str(value)
            + ('' if value.endswith(by) else by))


def asp_from_graph(graph, edge_predicate:str=edge_predicate) -> str:
    """Yield lines describing given graph"""
    for edge in graph.edges:
        yield '{}({},{}).'.format(edge_predicate, *map(as_asp_value, edge))
