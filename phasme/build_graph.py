
import networkx
import itertools
from collections import defaultdict
from phasme import commons
from phasme import graph_to_tex
from phasme.asp import asp_from_graph
from phasme.commons import edge_predicate, fixed_name
from phasme.extract_links import links_from_file, links_from_dirty_file
from phasme.extract_links import links_from_lines, links_from_dirty_lines


def graph_from_file(fname:str, edge_predicate:str=edge_predicate):
    fname = commons.normalize_filename(fname)
    if commons.format_of_file(fname) not in {'lp', ''}:
        return graph_from_standard_file(fname, edge_predicate=edge_predicate)
    graph = networkx.Graph()
    for edge in links_from_file(fname, edge_predicate=edge_predicate):
        graph.add_edge(*edge)
    return graph

def graph_from_standard_file(fname:str, edge_predicate:str=edge_predicate):
    """Build a graph from standard files"""
    fname = commons.normalize_filename(fname)
    ext = commons.format_of_file(fname)
    try:
        return getattr(networkx, 'read_' + ext)(fname)
    except AttributeError:
        raise ValueError("Given file format {} is not handled".format(ext))

def graph_from_dirty_file(fname:str, edge_predicate:str=edge_predicate):
    fname = commons.normalize_filename(fname)
    graph = networkx.Graph()
    for edge in links_from_dirty_file(fname, edge_predicate=edge_predicate):
        graph.add_edge(*edge)
    return graph


def graph_from_lines(lines:iter, edge_predicate:str=edge_predicate):
    graph = networkx.Graph()
    for edge in links_from_lines(lines, edge_predicate=edge_predicate):
        graph.add_edge(*edge)
    return graph

def graph_from_dirty_lines(lines:iter, edge_predicate:str=edge_predicate):
    graph = networkx.Graph()
    for edge in links_from_dirty_lines(lines, edge_predicate=edge_predicate):
        graph.add_edge(*edge)
    return graph


def graph_to_file(graph, fname:str, edge_predicate:str=edge_predicate, eol:str='\n'):
    """Write given graph into file, in clean ASP format."""
    format = commons.format_of_file(fname)
    if format not in {'lp', ''}:
        return graph_to_standard_file(graph, fname, format)
    with open(fname, 'w') as fd:
        for line in asp_from_graph(graph, edge_predicate=edge_predicate):
            fd.write(line + eol)
    return fname

def graph_to_standard_file(graph, fname:str, format:str):
    """Write given graph into file, in given standard format."""
    if format == 'dot':
        try:
            return networkx.drawing.nx_pydot.write_dot(graph, fname)
        except ImportError:
            return networkx.drawing.nx_agraph.write_dot(graph, fname)
    if format == 'tex':
        return graph_to_tex.graph_to_file(graph, fname)
    return getattr(networkx, 'write_' + format)(graph, fname)


def graph_from_networkx_method(method:str, method_parameters=[]):
    """Return a graph generated with given method and method parameters.

    method -- networkx attribute name implementing a graph generation method
    method_parameters -- iterable of string like '{field}={value}'

    """
    method_parameters = {
        field: float(value) if '.' in value else int(value)
        for field, value in map(lambda arg: arg.split('='), method_parameters)
    }
    return getattr(networkx, method)(**method_parameters)


def anonymized(graph):
    """Return a new graph, equivalent to given one but with node names changed
    to integers.
    """
    random_names = itertools.count(1)
    name = defaultdict(lambda: next(random_names))
    anon = type(graph)()
    for source, target in graph.edges:
        anon.add_edge(name[source], name[target])
    return anon


def normalized(graph, **fixed_name_kwargs):
    """Return a new graph, equivalent to given one but with node names changed
    to avoid any non alphanumeric character.
    """

    name_map = {n: fixed_name(n, keep_quotes=True, **fixed_name_kwargs) for n in graph.nodes}
    nb_new_names = sum(1 for _ in name_map.values())
    if len(name_map) != nb_new_names:
        diff = frozenset(name_map) - frozenset(name_map.values())
        raise RuntimeError("Normalization routine do not handle given graph. {} "
                           "nodes are lost because of name collision : "
                           "".format(len(diff), ', '.join(map(str, diff))))
    anon = type(graph)()
    for source, target in graph.edges:
        anon.add_edge(name_map[source], name_map[target])
    return anon
