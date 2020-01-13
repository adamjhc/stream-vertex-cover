"""
2k-Pass BST usingO(k·logn)bits
1-Pass BST usingO(k^2·logn)bits
"""
from networkx import Graph
from math import log2, ceil


def vertex_cover_branching_2k_pass(graph: Graph, k: int) -> set:
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


def vertex_cover_branching_1_pass(graph: Graph, k: int) -> set:
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
            Vertex cover if one exists otherwise None
    """
    pass


def _get_binary_strings(k: int) -> list:
    """
    Generates binary strings up to a given length k

    Parameters
    ----------
        k : int
            Length of binary strings to generate

    Returns
    -------
        list
            List of binary strings
    """
    return [bin(i)[2:].rjust(k, "0") for i in range(2 ** k)]


class _Node(object):
    def __init__(self, value, left=None, right=None):
        self.value = value  # The node value
        self.left = left  # Left child
        self.right = right  # Right child
