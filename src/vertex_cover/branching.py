"""
2k-Pass BST usingO(k·logn)bits
1-Pass BST usingO(k^2·logn)bits
"""
from networkx import Graph


def vertex_cover_branching_recursive(graph: Graph, k: int, vc: set = set()) -> set:
    """
    Finds a vertex cover of at most size k using branching

    Uses a recursive depth-first method

    Parameters
    ----------
        graph : Graph
            The graph to find a vertex cover of
        k : int
            Size k

    Returns
    -------
        set
    """
    if graph.number_of_edges() == 0:
        return vc

    if k == 0:
        return None

    (u, v) = list(graph.edges)[0]

    left_graph = graph.copy()
    left_graph.remove_node(u)
    left_vc = vc.copy()
    left_vc.add(u)
    left_vc = vertex_cover_branching(left_graph, k - 1, left_vc)

    if left_vc:
        return left_vc

    right_graph = graph.copy()
    right_graph.remove_node(v)
    right_vc = vc.copy()
    right_vc.add(v)
    right_vc = vertex_cover_branching(right_graph, k - 1, right_vc)
    return right_vc
