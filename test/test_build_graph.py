

import pytest
from .test_read_data import data_bad_complex
from grasp.build_graph import (graph_from_dirty_lines, graph_from_lines,
                               graph_from_file, graph_from_standard_file,
                               graph_from_networkx_method)


def comparable_graph(graph) -> frozenset:
    """Return a comparable between instances version of given networkx Graph"""
    return frozenset(map(frozenset, graph.edges))


def test_equality_of_methods(data_bad_complex):
    lines = data_bad_complex.splitlines()
    one = comparable_graph(graph_from_dirty_lines(lines))
    two = comparable_graph(graph_from_lines(lines))
    assert one == two


def test_gml():
    file = 'data/test.gml'
    one = comparable_graph(graph_from_file(file))
    two = comparable_graph(graph_from_standard_file(file))
    assert one == two


def test_graphml():
    file = 'data/test.graphml'
    one = comparable_graph(graph_from_file(file))
    two = comparable_graph(graph_from_standard_file(file))
    assert one == two
    assert one == frozenset(map(frozenset, ({'1', '2'}, {'1', '3'},
                                            {'2', '4'}, {'3', '4'})))


def test_generate_from_networkx():
    # NB: seed is here to enforce reproductibility
    graph = graph_from_networkx_method('powerlaw_cluster_graph',
                                       ['n=5', 'm=2', 'p=0.01', 'seed=42'])
    graph = comparable_graph(graph)
    assert len(graph) == 6
    assert graph == frozenset({frozenset({1, 2}), frozenset({1, 4}), frozenset({3, 4}), frozenset({2, 3}), frozenset({0, 2}), frozenset({1, 3})})
