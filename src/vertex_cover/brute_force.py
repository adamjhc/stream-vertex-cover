from networkx import Graph
from .util import powerset, is_vertex_cover


def vertex_cover_brute_force(
    graph: Graph, k: int = None, vertex_cover: set = None
) -> set:
    """
    Brute forces the subsets of the given graph to find a vertex cover

    Returns the first found vertex cover

    Parameters
    ----------
        graph : Graph 
            The graph to find a vertex cover of

    Returns
    -------
        set
    """
    if vertex_cover:
        nodes = set(graphs.nodes)
        nodes.difference_update(vertex_cover)
        for subset in map(set, powerset(nodes, k)):
            subset.update(vertex_cover)
            if is_vertex_cover(graph, subset):
                return subset
    else:
        for subset in map(set, powerset(list(graph.nodes), k)):
            if is_vertex_cover(graph, subset):
                return subset

    return None


def vertex_cover_brute_force_all(graph: Graph, k: int = None) -> set:
    """
    Brute forces the subsets of the given graph to find a vertex cover

    Returns all vertex covers found as a generator

    Parameters
    ----------
        graph : Graph
            The graph to find a vertex cover of

    Yields
    ------
        set
    """
    for subset in map(set, powerset(list(graph.nodes), k)):
        if is_vertex_cover(graph, subset):
            yield subset
