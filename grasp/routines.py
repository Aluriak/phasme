"""High level routines implementing the user-level behaviors.

"""

import os
import random
import networkx
from grasp import commons
from grasp.asp import asp_from_graph
from grasp.info import info
from grasp.commons import edge_predicate
from grasp.build_graph import graph_from_file, graph_to_file, graph_from_networkx_method, anonymized


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
            edge_predicate:str=edge_predicate,
            target_edge_predicate:str=edge_predicate) -> dict:
    """Write in target the very same graph as input, but in
    an clean ASP expanded format.

    anonymize -- rename nodes into integers.
    target -- file to write. If None or equal to fname, overwrite.
    target_edge_predicate -- edge predicate to use in rewritten file.

    """
    fname = commons.normalize_filename(fname)
    if target: target = commons.normalize_filename(target)
    if not target:  target = fname
    graph = graph_from_file(fname, edge_predicate=edge_predicate)
    if anonymize:  graph = anonymized(graph)
    graph_to_file(graph, target, edge_predicate=target_edge_predicate)


def generate(target:str, method:str, method_parameters=[],
             edge_predicate:str=edge_predicate):
    """Write in file of given name a graph generated with given method.

    """
    graph = graph_from_networkx_method(method, method_parameters)
    return graph_to_file(graph, target, edge_predicate=edge_predicate)
