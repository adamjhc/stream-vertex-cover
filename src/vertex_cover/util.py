from networkx import Graph


def powerset(seq: list):
    """
    Returns all the subsets of this set. This is a generator.

    Taken from: https://www.technomancy.org/python/powerset-generator-python/
    """
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]] + item
            yield item


def is_vertex_cover(graph: Graph, vertex_cover: set) -> bool:
    """
    Determines whether the given set of vertices is a vertex cover of the 
    given graph

    Loops through the graphs edges checking whether at least one end of the 
    edge is included in the vertex cover

    Parameters
    ----------
        graph : Graph
            The graph of which to check the vertex cover
        vertex_cover : set
            Set of vertices

    Returns
    -------
        bool
    """
    for (u, v) in graph.edges:
        if u not in vertex_cover and v not in vertex_cover:
            return False

    return True


def is_vertex_cover_alt(graph: Graph, vertex_cover: set) -> bool:
    """
    Determines whether the given set of vertices is a vertex cover of the 
    given graph

    Removes each vertex one by one from the graph and checks whether any edges 
    are left at the end

    Parameters
    ----------
        graph : Graph
            The graph of which to check the vertex cover
        vertex_cover :set
            Set of vertices

    Returns
    -------
        bool
    """
    graph.remove_nodes_from(vertex_cover)
    return graph.number_of_edges() == 0
