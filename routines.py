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



split_by_cc('data/three_cc.lp', 'out/three_cc_{}.lp')
