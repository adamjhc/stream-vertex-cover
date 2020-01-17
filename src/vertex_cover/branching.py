"""
2k-Pass BST usingO(k·logn)bits
1-Pass BST usingO(k^2·logn)bits
"""
from networkx import Graph


def vertex_cover_branching_recursive(graph: Graph, k: int, vc: set = set()) -> set:
    """
    Finds a vertex cover of at most size k using branching

    Uses a recursive depth-first preorder method

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

    graph_left = graph.copy()
    graph_left.remove_node(u)
    vc_left = vc.copy()
    vc_left.add(u)
    vc_left = vertex_cover_branching(graph_left, k - 1, vc_left)

    if vc_left:
        return vc_left

    graph_right = graph.copy()
    graph_right.remove_node(v)
    vc_right = vc.copy()
    vc_right.add(v)
    vc_right = vertex_cover_branching(graph_right, k - 1, vc_right)
    return vc_right
