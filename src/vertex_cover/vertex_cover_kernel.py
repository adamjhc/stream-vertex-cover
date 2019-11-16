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
"""


def vertex_cover_kernelization(graph, k):
    """
    Finds a vertex cover using kernelization with size k 

    Args:
        graph (Graph): Graph to perform on
        k (int): Size k

    Returns:
        Set of vertices that cover all edges
    """

    (kernel, vertexCover) = kernelize(graph, k)
    if len(kernel.vertices()) > k * (k + 1) or len(kernel.edges()) > k ** 2:
        return None

    return vertexCover + __brute_force(graph)


def kernelize(graph, k):
    """
    Kernelizes a graph given size k

    Args:
        k (int): Size k

    Returns:
        Pair of kernel and the partial vertex cover
    """

    vertexCover = set()
    kernel = graph
    while True:
        rulesApplied = False

        v = kernel.randomVertex()
        if k > 0 and v.degree() > k:
            vertexCover.add(v)
            kernel.remove(v)
            k -= 1
            rulesApplied = True

        if v.degree() == 0:
            kernel.remove(v)
            rulesApplied = True

        if not rulesApplied and len(kernel.edges()) > k ** 2:
            return None

    return (kernel, vertexCover)


def __brute_force(graph):
    vertices = graph.vertices()
    edges = graph.edges()

    for size in range(len(vertices)):
        vertexCovers = __generate_power_set(vertices, size)
        for vertexCover in vertexCovers:
            if __is_vertex_cover(edges, vertexCover):
                return vertexCover


def __generate_power_set(vertices, size):
    return []


def __is_vertex_cover(edges, vertexCover):
    return True


if __name__ == "__main__":
    pass
