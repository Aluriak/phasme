
import networkx
from asp import asp_from_graph
from commons import edge_predicate
from extract_links import links_from_file, links_from_dirty_file
from extract_links import links_from_lines, links_from_dirty_lines


def graph_from_file(fname:str, edge_predicate:str=edge_predicate):
    graph = networkx.Graph()
    for edge in links_from_file(fname, edge_predicate=edge_predicate):
        graph.add_edge(*edge)
    return graph

def graph_from_dirty_file(fname:str, edge_predicate:str=edge_predicate):
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
    with open(fname, 'w') as fd:
        for line in asp_from_graph(graph, edge_predicate=edge_predicate):
            fd.write(line + eol)
