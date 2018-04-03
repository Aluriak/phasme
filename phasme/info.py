"""Implementation of info extraction related functions.

"""

import networkx
from inspect import getfullargspec
from collections import OrderedDict
from phasme import commons
from phasme.commons import edge_predicate
from phasme.build_graph import graph_from_file


def yield_info(fname:str, info_motifs:int=0, info_ccs:bool=True,
               graphics:bool=False, outdir:str='.',
               special_nodes:bool=False,
               heavy_computations:bool=False, graph_properties:bool=False,
               negative_results:bool=True,
               edge_predicate:str=edge_predicate) -> dict:
    """Yield (field, value) infos of targets written

    info_motifs -- print info about the n first motifs in the graph
    info_ccs -- print info about connected components in the graph

    """
    outdir = commons.normalize_filename(outdir)
    graph = graph_from_file(fname, edge_predicate=edge_predicate)
    nb_node, nb_edge = len(graph.nodes), len(graph.edges)
    nb_self_loops = sum(1 for _ in graph.selfloop_edges())
    def density(nb_node, nb_edge):
        try:
            return 2 * nb_edge / (nb_node * (nb_node - 1))
        except ZeroDivisionError:
            import math
            return math.nan

    yield '#node', nb_node
    yield '#edge', nb_edge
    if nb_self_loops:
        yield '#loop', nb_self_loops
        yield '#edge - #loop', nb_edge - nb_self_loops
    else:
        yield 'no loop', True
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
        # TODO: degree function to clustering coefficient
        ...

    if heavy_computations:
        # TODO: concept and AOC poset size and ratio.
        ...

    if special_nodes:
        # TODO: equivalences
        arti_points = tuple(networkx.articulation_points(graph))
        yield '#articulation points', len(arti_points)
        if arti_points:
            yield 'articulation points', arti_points

    if graph_properties:
        non_implemented = []
        for attrname, attr in vars(networkx).items():
            if attrname.startswith('is_'):
                attrname = attrname[3:]
                if getfullargspec(attr).args == ['G']:  # only 1 arg
                    try:
                        yield attrname, attr(graph)  # discard the 'is_'
                    except networkx.exception.NetworkXNotImplemented as err:
                        non_implemented.append(attrname)
                    except networkx.exception.NetworkXError as err:
                        non_implemented.append(attrname)

        properties = ('transitivity', 'average_clustering', 'average_node_connectivity', 'average_shortest_path_length')
        for attrname in properties:
            try:
                yield attrname, getattr(networkx, attrname)(graph)
            except networkx.exception.NetworkXError as err:
                non_implemented.append(attrname)
        if non_implemented and negative_results:
            yield 'non implemented', non_implemented


def info(fname:str, info_motifs:int=0, info_ccs:bool=True,
         graphics:bool=False, outdir:str='.',
         special_nodes:bool=False, heavy_computations:bool=False,
         graph_properties:bool=False,
         round_float:int=None,
         negative_results:bool=True, edge_predicate:str=edge_predicate) -> dict:
    """Yield lines of text describing given graph info."""
    infos = OrderedDict(yield_info(fname, info_motifs, info_ccs, graphics, outdir, special_nodes, heavy_computations, graph_properties, negative_results, edge_predicate))
    properties = {True: set(), False: set()}
    maxkeylen = max(map(len, infos))
    iter_handler = lambda v: ', '.join(sorted(map(str, v)))
    type_handler = {
        str: str,
        tuple: iter_handler,
        list: iter_handler,
        set: iter_handler,
        int: str,
        float: (str if round_float is None else lambda v, r=round_float: str(round(v, r))),
    }
    def show(field, value, maxkeylen=maxkeylen):
        return field.rjust(maxkeylen+2) + ' | ' + type_handler[type(value)](value)

    for field, value in infos.items():
        if isinstance(value, bool):
            properties[value].add(field)
        else:
            yield show(field, value)
    if negative_results and properties[False]:
        yield show('¬properties', properties[False])
    if properties[True]:
        yield show('properties', properties[True])
