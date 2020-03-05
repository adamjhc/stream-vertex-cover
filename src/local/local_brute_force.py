from typing import Iterator, Optional, cast

from networkx import Graph

from local_util import is_vertex_cover, powerset


def vertex_cover_brute_force(
    graph: Graph, k: int = None, vertex_cover: set = None
) -> Optional[set]:
    """
    Brute forces the subsets of the given graph to find a vertex cover

    Returns the first found vertex cover

    Parameters
    ----------
        graph : Graph
            The graph to find a vertex cover of
        k : int
            Maximum size k [Default: None]
        vertex_cover : set
            Partial vertex cover if one exists [Default: None]

    Returns
    -------
        Optional[set]
            Vertex cover if one exists else `None`
    """
    if vertex_cover:
        nodes = set(graph.nodes)
        nodes.difference_update(vertex_cover)
        for subset in map(set, powerset(list(nodes), k)):
            subset.update(vertex_cover)
            if is_vertex_cover(graph, subset):
                return subset
    else:
        for subset in map(set, powerset(list(graph.nodes), k)):
            if is_vertex_cover(graph, subset):
                return subset

    return None


def vertex_cover_brute_force_all(graph: Graph, k: int = None) -> Iterator[set]:
    """
    Brute forces the subsets of the given graph to find a vertex cover

    Returns all vertex covers found as a generator

    Parameters
    ----------
        graph : Graph
            The graph to find a vertex cover of
        k : int
            Maximum size k [Default: None]

    Yields
    ------
        set
            Vertex cover
    """
    for subset in map(set, powerset(list(graph.nodes), k)):
        if is_vertex_cover(graph, subset):
            yield subset
