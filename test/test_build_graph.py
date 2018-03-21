

import pytest
from .test_read_data import data_bad_complex
from build_graph import graph_from_dirty_lines, graph_from_lines


def test_equality_of_methods(data_bad_complex):
    lines = data_bad_complex.splitlines()
    one = map(frozenset, graph_from_dirty_lines(lines).edges)
    two = map(frozenset, graph_from_lines(lines).edges)
    assert set(one) == set(two)
