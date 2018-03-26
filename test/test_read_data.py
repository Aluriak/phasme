

import pytest
from phasme.extract_links import links_from_clean_lines, links_from_lines


@pytest.fixture
def data_good_complex():
    return """
edge(a,b). 
edge(c,d). % this line should be ignored (as previous trailing space)
% so is this one
edge("alé-<ltaxq,ru()",a01982_29823tele).% awful!
"""

@pytest.fixture
def data_bad_complex():
    return """
edge(a,b).
edge(c,d). edge(e,f).
edge("alé-<ltaxq,ru()",a01982_29823tele).% awful!
"""


def test_read_bad_complex_asp_data(data_bad_complex):
    expected = {('a', 'b'), ('c', 'd'), ('e', 'f'), ('"alé-<ltaxq,ru()"', 'a01982_29823tele')}
    found = set(links_from_lines(data_bad_complex.splitlines()))
    assert found == expected


def test_read_good_complex_asp_data(data_good_complex):
    expected = (('a', 'b'), ('c', 'd'), ('"alé-<ltaxq,ru()"', 'a01982_29823tele'))
    found = tuple(links_from_clean_lines(data_good_complex.splitlines()))
    assert found == expected


def test_read_comments_without_handling(data_good_complex):
    with pytest.raises(ValueError) as err:
        tuple(links_from_clean_lines(data_good_complex.splitlines(), handle_comments=False))
    assert str(err.value) == "Non compliant ASP data: '{}'".format(data_good_complex.splitlines()[2].strip())


def test_read_badly_formed_asp_data():
    data = "edge(a,b). edge(c,d)."
    with pytest.raises(ValueError) as err:
        tuple(links_from_clean_lines(data.splitlines()))
    assert str(err.value) == "Non compliant ASP data: '{}'".format(data)

