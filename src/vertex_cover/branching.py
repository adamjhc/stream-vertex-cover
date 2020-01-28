"""
2k-Pass BST usingO(k·logn)bits
1-Pass BST usingO(k^2·logn)bits
"""
from networkx import Graph
from collections import deque


def vertex_cover_branching(graph: Graph, k: int, vc: set = set()) -> set:
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


def vertex_cover_branching_stream(graph: Graph, k: int) -> set:
    """
    Finds a vertex cover of at most size k using branching

    Algorithm from Chitnis and Cormode 2019 - Towards a Theory of Parameterized
    Streaming Algorithms

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
    no_of_edges = len(edges)

    # each loop acts as another pass
    for bin_string in _get_binary_strings(k):
        vertex_cover = set()
        bin_string_pos = 1
        edge_pos = 1
        while bin_string_pos != k + 1:
            (u, v) = edges[edge_pos - 1]
            if u not in vertex_cover and v not in vertex_cover:
                # FIXME: check if u is less than v in a type safe way
                if bin_string[bin_string_pos - 1] == "0":
                    vertex_cover.add(u)
                else:
                    vertex_cover.add(v)
                bin_string_pos += 1
            edge_pos += 1

        if edge_pos == no_of_edges + 1:
            return vertex_cover

    return None


def vertex_cover_branching_dfs_iterative(graph: Graph, k: int) -> set:
    """
    Finds a vertex cover of at most size k using branching

    Uses an iterative depth-first method

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
    stack = []
    stack.append((graph, set()))

    while len(stack) > 0:
        graph, vc = stack.pop()

        if graph.number_of_edges() == 0:
            return vc

        if len(vc) == k:
            continue

        u, v = list(graph.edges)[0]

        graph_left = graph.copy()
        graph_left.remove_node(u)
        vc_left = vc.copy()
        vc_left.add(u)
        stack.append((graph_left, vc_left))

        graph_right = graph.copy()
        graph_right.remove_node(u)
        vc_right = vc.copy()
        vc_right.add(u)
        stack.append((graph_right, vc_right))

    return None


def vertex_cover_branching_bfs(graph: Graph, k: int) -> set:
    """
    Finds a vertex cover of at most size k using branching

    Uses an iterative breadth-first method

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
    queue = deque()
    queue.append((graph, set()))

    while len(queue) > 0:
        graph, vc = queue.popleft()

        if graph.number_of_edges() == 0:
            return vc

        if len(vc) == k:
            continue

        u, v = list(graph.edges)[0]

        graph_left = graph.copy()
        graph_left.remove_node(u)
        vc_left = vc.copy()
        vc_left.add(u)
        queue.append((graph_left, vc_left))

        graph_right = graph.copy()
        graph_right.remove_node(u)
        vc_right = vc.copy()
        vc_right.add(u)
        queue.append((graph_right, vc_right))

    return None


def _get_binary_strings(k: int) -> list:
    """
    Generates binary strings up to a given length k

    Parameters
    ----------
        k : int
            Length of binary strings to generate

    Yields
    ------
        list
            List of binary strings
    """
    for i in range(2 ** k):
        yield bin(i)[2:].rjust(k, "0")
