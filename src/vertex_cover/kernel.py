"""
Kernelization Algorithm for Vertex Cover
(from https://en.wikipedia.org/wiki/Kernelization#Example:_vertex_cover)

1.  If k > 0 and v is a vertex of degree > k, remove v from the graph and 
    decrease k by 1. Every vertex of size k must contain v since otherwise too 
    many of its neighbours would have to be picked to cover the incident edges. 
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
from networkx import Graph
from .brute_force import vertex_cover_brute_force


def vertex_cover_kernelization(graph: Graph, k: int) -> set:
    """
    Finds a vertex cover of size k using kernelization

    Returning a set of at most k vertices that includes the endpoint of every 
    edge in the graph or None if no such set exists

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
    kernel = _kernelize(graph, k)
    if not kernel:
        return None

    return vertex_cover_brute_force(kernel)


def _kernelize(graph: Graph, k: int) -> Graph:
    """
    Kernelizes a graph given size k 

    Parameters
    ----------
        graph : Graph
            Graph to kernelize
        k : int
            Size k

    Returns
    -------
        Graph
    """
    kernel = graph
    reductionsCanBeMade = True
    while reductionsCanBeMade:
        reductionMade = False
        for node in list(kernel.nodes):
            if k > 0 and kernel.degree[node] > k:
                reductionMade = True
                kernel.remove_node(node)
                k -= 1
            elif kernel.degree[node] == 0:
                reductionMade = True
                kernel.remove_node(node)
            elif kernel.number_of_edges() > k ** 2:
                return None

        if not reductionMade:
            reductionsCanBeMade = False

    return kernel


if __name__ == "__main__":
    pass
