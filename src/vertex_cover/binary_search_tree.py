"""
2k-Pass BST usingO(k·logn)bits
1-Pass BST usingO(k^2·logn)bits
"""
from networkx import Graph


def vertex_cover_bst_2k_pass(graph: Graph, k: int) -> set:
    """
    Finds a vertex cover of size k using a binary search tree

    Essentially a depth-first search of a binary search tree

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
    pass


def vertex_cover_bst_1_pass(graph: Graph, k: int) -> set:
    """
    Finds a vertex cover of size k using a binary search tree

    Essentially a breadth-first search of a binary search tree

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
    pass
