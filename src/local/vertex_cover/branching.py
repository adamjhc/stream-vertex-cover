"""
2k-Pass BST usingO(k·logn)bits
1-Pass BST usingO(k^2·logn)bits
"""
from typing import Optional, List, Iterator
from networkx import Graph
from collections import deque


def vertex_cover_branching(
    graph: Graph, k: int, vertex_cover: set = set()
) -> Optional[set]:
    """
    Finds a vertex cover of at most size k using branching

    Uses a recursive depth-first preorder method

    Parameters
    ----------
        graph : Graph
            The graph to find a vertex cover of
        k : int
            Size k
        vertex_cover : set
            Current Vertex Cover - [Default: `set()`]
        
    Returns
    -------
        Optional[set]
            Vertex cover is one exists else `None`
    """
    if graph.number_of_edges() == 0:
        return vertex_cover

    if k == 0:
        return None

    (u, v) = list(graph.edges)[0]

    left_graph = graph.copy()
    left_graph.remove_node(u)
    left_current_vc = vertex_cover.copy()
    left_current_vc.add(u)
    vc_left = vertex_cover_branching(left_graph, k - 1, left_current_vc)

    if vc_left:
        return vc_left

    right_graph = graph.copy()
    right_graph.remove_node(v)
    right_current_vc = vertex_cover.copy()
    right_current_vc.add(v)
    vc_right = vertex_cover_branching(right_graph, k - 1, right_current_vc)
    return vc_right


def vertex_cover_branching_stream(graph: Graph, k: int) -> Optional[set]:
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
        Optional[set]
            Vertex cover is one exists else `None`
    """
    edges = list(graph.edges)
    no_of_edges = len(edges)

    # each loop acts as another pass
    for bin_string in _get_binary_strings(k):
        vertex_cover: set = set()
        bin_string_pos = 1
        edge_pos = 1
        while bin_string_pos != k + 1:
            (u, v) = edges[edge_pos - 1]
            if u not in vertex_cover and v not in vertex_cover:
                edge_sm, edge_bg = (u, v) if u < v else v, u
                if bin_string[bin_string_pos - 1] == "0":
                    vertex_cover.add(edge_sm)
                else:
                    vertex_cover.add(edge_bg)
                bin_string_pos += 1
            edge_pos += 1

        if edge_pos == no_of_edges + 1:
            return vertex_cover

    return None


def vertex_cover_branching_dfs_iterative(graph: Graph, k: int) -> Optional[set]:
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
        Optional[set]
            Vertex cover is one exists else `None`
    """
    stack: List = []
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


def vertex_cover_branching_bfs(graph: Graph, k: int) -> Optional[set]:
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
        Optional[set]
            Vertex cover is one exists else `None`
    """
    queue: deque = deque()
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


def _get_binary_strings(k: int) -> Iterator[str]:
    """
    Generates binary strings up to a given length k

    Parameters
    ----------
        k : int
            Length of binary strings to generate

    Yields
    ------
        str
            Incrementing Binary strings
    """
    for i in range(2 ** k):
        yield bin(i)[2:].rjust(k, "0")
