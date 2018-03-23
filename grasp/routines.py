"""High level routines implementing the user-level behaviors.

"""

import os
import networkx
from grasp import commons
from grasp.asp import asp_from_graph
from grasp.commons import edge_predicate
from grasp.build_graph import graph_from_file, graph_to_file


def split_by_cc(fname:str, targets:str=None, edge_predicate:str=edge_predicate) -> tuple:
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
    for idx, cc_nodes in enumerate(networkx.connected_components(graph)):
        cc = graph.subgraph(cc_nodes)
        target = targets.format(idx)
        with open(target, 'w') as fd:
            for line in asp_from_graph(cc, edge_predicate=edge_predicate):
                fd.write(line+'\n')
        writtens.append(target)
    return tuple(writtens)


def clean(fname:str, target:str=None,
          edge_predicate:str=edge_predicate,
          target_edge_predicate:str=edge_predicate) -> dict:
    """Write in target the very same graph as input, but in
    an clean ASP expanded format.

    target -- file to write. If None or equal to fname, overwrite.
    target_edge_predicate -- edge predicate to use in rewritten file.

    """
    fname = commons.normalize_filename(fname)
    if target: target = commons.normalize_filename(target)
    if not target:  target = fname
    graph = graph_from_file(fname, edge_predicate=edge_predicate)
    graph_to_file(graph, target, edge_predicate=target_edge_predicate)


def info(fname:str, info_motifs:int=0, info_ccs:bool=True,
         graphics:bool=False, outdir:str='.',
         heavy_computations:bool=False,
         edge_predicate:str=edge_predicate) -> dict:
    """Yield (field, value) infos of targets written

    info_motifs -- print info about the n first motifs in the graph
    info_ccs -- print info about connected components in the graph

    """
    outdir = commons.normalize_filename(outdir)
    graph = graph_from_file(fname, edge_predicate=edge_predicate)
    nb_node, nb_edge = len(graph.nodes), len(graph.edges)
    def density(nb_node, nb_edge):
        try:
            return 2 * nb_edge / (nb_node * (nb_node - 1))
        except ZeroDivisionError:
            import math
            return math.nan

    yield '#node', nb_node
    yield '#edge', nb_edge
    yield 'density', density(nb_node, nb_edge)

    if info_motifs:
        for motif in ():
            clyngor.solve()
    if info_ccs:
        ccs_nodes = tuple(networkx.connected_components(graph))
        ccs = tuple(graph.subgraph(cc) for cc in ccs_nodes)
        yield '#cc', len(ccs_nodes)
        if len(ccs_nodes) > 1:
            node_per_cc = tuple(map(len, ccs_nodes))
            yield '#node/cc', node_per_cc
            yield '#node/cc (prop)', tuple(nb / nb_node for nb in node_per_cc)
            yield '#node/cc (mean)', sum(node_per_cc) / len(node_per_cc)
            yield 'density/cc', tuple(density(len(nodes), len(tuple(cc.edges))) for cc, nodes in zip(ccs, ccs_nodes))


    if graphics:
        # TODO: degree distribution (lin-lin, log-lin, lin-log, log-log)
        # TODO: motif size distribution (if info_motifs > 1)
        ...

    if heavy_computations:
        # TODO: bipartite detection
        # TODO: concept and AOC poset size, ratio.
        ...
