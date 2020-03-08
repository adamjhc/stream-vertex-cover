from typing import Any, Callable, Collection, Tuple

import networkx as nx
from networkx import Graph


def _in(item: Any, pairs: Collection[Tuple[Any, Any]]) -> bool:
    for pair in pairs:
        if item in pair:
            return True

    return False


def get_read_func_from_edgelist(path: str) -> Callable:
    """Gets the appropriate NetworkX read edgelist function for a given
    edgelist

    Arguments
    ---------
        path : str
            Path to the edgelist

    Returns
    -------
        Callable
            NetworkX read_edgelist or read_weighted_edgelist
    """
    read_func = nx.read_edgelist
    with open(path, "r") as edgelist:
        line = edgelist.readline()
        if len(line.split()) > 2:
            read_func = nx.read_weighted_edgelist

    return read_func


def get_graph_layout(graph: Graph) -> dict:
    """Returns an appropriate NetworkX graph layout

    Kamada-Kawai runs out of memory for larger graphs so spring is used as a
    fallback

    Arguments
    ---------
        graph : Graph
            Graph to generate layout from

    Returns
    -------
        dict
            Dictionary containing positions of nodes
    """
    if graph.number_of_edges() < 1000:
        return nx.kamada_kawai_layout(graph)
    else:
        return nx.spring_layout(graph)
