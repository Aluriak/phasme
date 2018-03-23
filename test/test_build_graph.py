

import pytest
from .test_read_data import data_bad_complex
from grasp.build_graph import (graph_from_dirty_lines, graph_from_lines,
                               graph_from_file, graph_from_standard_file)


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
