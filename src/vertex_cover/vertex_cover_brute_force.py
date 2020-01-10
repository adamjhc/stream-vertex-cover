from .vertex_cover_util import powerset, is_vertex_cover


def vertex_cover_brute_force(graph: Graph):
    """
    Brute forces the subsets of the given graph to find a vertex cover

    Returns the first found vertex cover

    Args:
    - graph (Graph): The graph to find a vertex cover of

    Returns:
    - set
    """
    ps_vertices = powerset(list(graph.nodes))
    for vertex_cover in ps_vertices:
        if is_vertex_cover(graph, vertex_cover):
            return vertex_cover

    assert False, "This graph doesn't have a vertex cover?"


def vertex_cover_brute_force_all(graph: Graph):
    """
    Brute forces the subsets of the given graph to find a vertex cover

    Returns all vertex covers found as a generator

    Args:
    - graph (Graph): The graph to find a vertex cover of

    Returns:
    - list
    """
    ps_vertices = powerset(list(graph.nodes))
    for vertex_cover in ps_vertices:
        if is_vertex_cover(graph, vertex_cover):
            yield vertex_cover
