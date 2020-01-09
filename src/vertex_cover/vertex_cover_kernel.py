"""
Kernel Algorithm for Vertex Cover
(from https://en.wikipedia.org/wiki/Kernelization#Example:_vertex_cover)

1.  If k > 0 and v is a vertex of degree > k, remove v from the graph and 
    decrease k by 1. Every vertex of size k must contain v since otherwise too 
    many of its neighbors would have to be picked to cover the incident edges. 
    Thus, an optimal vertex cover for the original graph may be formed from a 
    cover of the reduced problem by adding v back to the cover
2.  If v is an isolated vertex, remove it. An isolated vertex cannot cover any 
    edges, so in this case v cannot be part of any minimal cover
3.  If more than k^2 edges remain in the graph, and neither of the previous two
    rules can be applied, then the graph cannot contain a vertex cover of size 
    k. For, after eliminating all vertices of degree > k, each remaining vertex
    can only cover at most k edges and a set of k vertices could only cover at 
    most k^2 edges. In this case, the instance may be replaced by an instance 
    with two vertices, one edge, and k=0, which also has no solution.

An algorithm that applies these rules repeatedly until no more reductions can 
be made necessarily terminates with a kernel that has at most k^2 edges and 
(because each edge has at most two endpoints and there are no isolated 
vertices) at most 2k^{2} vertices. This kernelization may be implemented in 
linear time. Once the kernel has been constructed, the vertex cover problem may
be solved by a brute force search algorithm that tests whether each subset of 
the kernel is a cover of the kernel. Thus, the vertex cover problem can be 
solved in time O(2^{{2k^{2}}}+n+m) for a graph with n vertices and m edges, 
allowing it to be solved efficiently when k is small even if n and m are both 
large.
"""
from typing import Tuple

import networkx as nx
from networkx import Graph
from networkx.algorithms.approximation.vertex_cover import min_weighted_vertex_cover
from networkx.classes.function import number_of_edges


def vertex_cover_kernelization(graph: Graph, k: int) -> set:
    """
    Finds a vertex cover of size k using kernelization

    Args:
    - graph (Graph): Graph to perform on
    - k (int): Size k

    Returns:
    - Set of at most k vertices that includes the endpoint of every edge in the
      graph or None if no such set exists
    """

    kernel = _kernelize(graph, k)
    # if len(kernel.vertices()) > k * (k + 1) or len(kernel.edges()) > k ** 2:
    #     return None

    # Once the kernel has been constructed, the vertex cover problem may be 
    # solved by a brute force search algorithm that tests whether each subset of 
    # the kernel is a cover of the kernel.
    # return min_weighted_vertex_cover(kernel)
    


def _kernelize(graph: Graph, k: int) -> Graph:
    """
    Kernelizes a graph given size k 

    Args:
    - graph (Graph): Graph to kernelize
    - k (int): Size k

    Returns:
    - kernel (Graph): Kernelized graph
    """

    kernel = graph
    reductionsCanBeMade = True
    while reductionsCanBeMade:
        v = kernel.randomVertex()
        if k > 0 and v.degree() > k:
            kernel.remove(v)
            k -= 1
        elif v.degree() == 0:
            kernel.remove(v)
        elif number_of_edges(kernel) > k ** 2:
            return None
        else:
            reductionsCanBeMade = False

    return kernel


if __name__ == "__main__":
    pass
