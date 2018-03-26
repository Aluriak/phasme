from phasme.routines import info


def test_infos():
    assert tuple(info('data/test.gml')) == tuple(EXPECTED_SIMPLE)

def test_infos_with_properties():
    assert tuple(info('data/test.gml', graph_properties=True, negative_results=False, round_float=2)) == tuple(EXPECTED_PROPERTIES)

def test_infos_with_properties_and_negative():
    assert tuple(info('data/test.gml', graph_properties=True, negative_results=True, round_float=2)) == tuple(EXPECTED_PROPERTIES_AND_NEGATIVES)


EXPECTED_SIMPLE = """
   #node | 11
   #edge | 19
 density | 0.34545454545454546
     #cc | 1
""".splitlines(False)[1:]

EXPECTED_PROPERTIES = """
                        #node | 11
                        #edge | 19
                      density | 0.35
                          #cc | 1
                 transitivity | 0.59
           average_clustering | 0.6
    average_node_connectivity | 1.78
 average_shortest_path_length | 2.0
                   properties | chordal, connected
""".splitlines(False)[1:]

EXPECTED_PROPERTIES_AND_NEGATIVES = """
                        #node | 11
                        #edge | 19
                      density | 0.35
                          #cc | 1
                 transitivity | 0.59
           average_clustering | 0.6
    average_node_connectivity | 1.78
 average_shortest_path_length | 2.0
              non implemented | aperiodic, arborescence, attracting_component, branching, semiconnected, strongly_connected, weakly_connected
                  ¬properties | biconnected, bipartite, directed, directed_acyclic_graph, distance_regular, empty, eulerian, forest, frozen, strongly_regular, tree
                   properties | chordal, connected
""".splitlines(False)[1:]
