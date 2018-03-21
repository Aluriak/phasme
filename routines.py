"""High level routines implementing the user-level behaviors.

"""

import os
import networkx
from asp import asp_from_graph
from commons import edge_predicate
from build_graph import graph_from_file


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


def info(fname:str, info_motifs:int=0, info_ccs:bool=True,
         edge_predicate:str=edge_predicate) -> dict:
    """Yield (field, value) infos of targets written

    info_motifs -- print info about the n first motifs in the graph
    info_ccs -- print info about connected components in the graph

    """
    graph = graph_from_file(fname, edge_predicate=edge_predicate)
    nb_node, nb_edge = len(graph.nodes), len(graph.edges)
    def density(nb_node, nb_edge):
        return 2 * nb_edge / (nb_node * (nb_node - 1))

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
        node_per_cc = tuple(map(len, ccs_nodes))
        yield '#node/cc', node_per_cc
        yield '#node/cc (prop)', tuple(nb / nb_node for nb in node_per_cc)
        yield '#node/cc (mean)', sum(node_per_cc) / len(node_per_cc)
        yield 'density/cc', tuple(density(len(nodes), len(tuple(cc.edges))) for cc, nodes in zip(ccs, ccs_nodes))

