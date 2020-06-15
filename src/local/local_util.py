from itertools import combinations
from typing import Any, Collection, Iterator, Sequence, Tuple
from warnings import warn

from networkx import Graph


def powerset(seq: Sequence, k: int = None) -> Iterator[list]:
    """
    Returns all subsets up to a size of k of a given set

    Returns all subsets if no k is given

    Parameters
    ----------
        seq : list
            List to generate subsets of
        k : int
            Maximum size of subset

    Yields
    ------
        list
            Subset
    """
    if k:
        for i in range(k + 1):
            for subset in combinations(seq, i):
                yield list(subset)
    else:
        # Taken from:
        # https://www.technomancy.org/python/powerset-generator-python/
        if len(seq) <= 1:
            yield list(seq)
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


def item_in(item: Any, pairs: Collection[Tuple[Any, Any]]) -> bool:
    """Checks whether an item exists anywehre in a collection of pairs

    Arguments
    ---------
        item : Any
            Item to look for
        pairs : Collection[Tuple[Any, Any]]
            Collections of pairs to look in

    Returns
    -------
        bool
            True/False whether item was found
    """
    for pair in pairs:
        if item in pair:
            return True

    return False
