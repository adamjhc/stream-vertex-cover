"""
2k-Pass BST usingO(k·logn)bits
1-Pass BST usingO(k^2·logn)bits
"""
from networkx import Graph


def vertex_cover_branching_2k_pass(graph: Graph, k: int) -> set:
    """
    Finds a vertex cover of size k using branching

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
    edges = list(graph.edges)

    # each loop acts as another pass
    for x in _get_binary_strings(k):
        S = set()
        i = 0
        j = 0
        while i != k + 1:
            (u, v) = edges[j]
            if u not in S and v not in S:
                if x[i] == "0":
                    S.add(u)
                else:
                    S.add(v)
                i += 1
            j += 1

        if j == m + 1:
            return S

    return None


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
