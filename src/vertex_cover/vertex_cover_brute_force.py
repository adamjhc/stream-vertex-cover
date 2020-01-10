"""
"Once the kernel has been constructed, the vertex cover problem may be solved 
by a brute force search algorithm that tests whether each subset of the kernel 
is a cover of the kernel."
"""

from .vertex_cover_util import powerset, is_vertex_cover


def vertex_cover_brute_force(graph: Graph):
    """
    Tests all subsets of a given graph's nodes to check if any are a vertex 
    cover of the given graph

    Args:
    - graph (Graph): The graph to find a vertex cover of

    Returns:
    - set
    """
    ps_vertices = powerset(list(graph.nodes))
    for vertex_cover in ps_vertices:
        if is_vertex_cover(graph, vertex_cover):
            return vertex_cover
