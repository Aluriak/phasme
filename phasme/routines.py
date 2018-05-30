"""High level routines implementing the user-level behaviors.

"""

import os
import random
import networkx
import itertools
from phasme import commons
from phasme.asp import asp_from_graph
from phasme.info import info
from phasme.commons import edge_predicate
from phasme.build_graph import graph_from_file, graph_to_file, graph_from_networkx_method, anonymized, normalized


def split_by_cc(fname:str, targets:str=None, order:str=None, slice=None,
                edge_predicate:str=edge_predicate) -> tuple:
    """Return names of targets written"""
    if not targets:
        name, ext = os.path.splitext(fname)
        targets = name + '_{}' + ext
    elif not isinstance(targets, str):
        raise ValueError("Target should be a filename to write")
    elif '{}' not in targets:
        raise ValueError("Target should be a filename to write containing '{}'")
    graph = graph_from_file(fname, edge_predicate=edge_predicate)
    writtens = []
    ccs = networkx.connected_components(graph)
    if order in {'biggest first', 'smaller last'}:
        ccs = sorted(tuple(ccs), key=len, reverse=True)
    elif order in {'biggest last', 'smaller first'}:
        ccs = sorted(tuple(ccs), key=len)
    elif order == 'random':
        ccs = list(ccs)
        random.shuffle(ccs)
    if slice:
        try:
            if len(slice) != 2 or any(not isinstance(v, int) for v in slice):
                raise TypeError  # trigger the exception handling
        except TypeError:  # slice is not iterable
            raise ValueError("Slice must be an iterable of two integers")
        start, end = slice
        ccs = tuple(ccs)[start:end]
    for idx, cc_nodes in enumerate(ccs, start=1):
        cc = graph.subgraph(cc_nodes)
        target = targets.format(idx)
        graph_to_file(cc, target)
        writtens.append(target)
    return tuple(writtens)


def convert(fname:str, target:str=None, anonymize:bool=False,
            normalize:bool=False, edge_predicate:str=edge_predicate,
            target_edge_predicate:str=edge_predicate) -> dict:
    """Write in target the very same graph as input, but in
    an clean ASP expanded format.

    normalize -- avoid special characters in node names.
    anonymize -- rename nodes into integers.
    target -- file to write. If None or equal to fname, overwrite.
    target_edge_predicate -- edge predicate to use in rewritten file.

    """
    fname = commons.normalize_filename(fname)
    if target: target = commons.normalize_filename(target)
    if not target:  target = fname
    graph = graph_from_file(fname, edge_predicate=edge_predicate)
    if anonymize:  graph = anonymized(graph)
    if normalize:  graph = normalized(graph)
    graph_to_file(graph, target, edge_predicate=target_edge_predicate)


def generate(target:str, method:str, method_parameters=[],
             edge_predicate:str=edge_predicate):
    """Write in file of given name a graph generated with given method.

    """
    graph = graph_from_networkx_method(method, method_parameters)
    return graph_to_file(graph, target, edge_predicate=edge_predicate)


def extract_by_node(fname:str, target:str=None, nodes:iter=(), order:int=1,
                    edge_predicate:str=edge_predicate):
    """Write in file of given name a subgraph of input one.

    """
    fname = commons.normalize_filename(fname)
    if target: target = commons.normalize_filename(target)
    if not target:  target = fname
    graph = graph_from_file(fname, edge_predicate=edge_predicate)
    nodes = set(nodes)
    all_neighbors = networkx.classes.function.all_neighbors
    for _ in range(order):
        nodes |= set(itertools.chain.from_iterable(
            all_neighbors(graph, node) for node in nodes
        ))
    return graph_to_file(graph.subgraph(nodes), target, edge_predicate=edge_predicate)


def randomize(fname:str, target:str, iterations:int, per_cc:bool=False,
              edge_predicate:str=edge_predicate):
    """Write in file of given name a randomized version of input graph.

    """
    fname = commons.normalize_filename(fname)
    target = commons.normalize_filename(target)
    graph = graph_from_file(fname, edge_predicate=edge_predicate)
    if per_cc:
        graphs = (
            graph.subgraph(nodes).copy()
            for nodes in networkx.connected_components(graph)
        )
    else:
        graphs = [graph]
    def run():
        for graph in graphs:
            print(tuple(graph.edges))
            nb_edge = graph.number_of_edges()
            total_iterations = iterations * graph.number_of_edges()
            try:
                yield networkx.algorithms.double_edge_swap(graph, nswap=total_iterations, max_tries=100*total_iterations)
            except networkx.exception.NetworkXError as err:
                print(err.args[0])
                yield graph
            except networkx.exception.NetworkXAlgorithmError:
                print("Maximum number of swap attempts reached, or graph can't be swapped. Ignored.")
                yield graph
    if per_cc:
        graph = networkx.compose_all(run())
    else:
        graph = next(run())
    return graph_to_file(graph, target, edge_predicate=edge_predicate)
