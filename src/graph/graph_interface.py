from typing import TypeVar, Generic, Set, Tuple

Vertex = TypeVar("Vertex")
Edge = Tuple[Vertex, Vertex]


class Graph(Generic[Vertex]):
    """
    Graph Interface
    """

    def vertices(self) -> Set[Vertex]:
        """
        Returns:
            Set of vertices in the graph
        """
        raise NotImplementedError()

    def edges(self) -> Set[Edge]:
        """
        Returns:
            Set of all edges as pairs in the graph
        """
        raise NotImplementedError()

    def add_vertex(self, vertex: Vertex) -> None:
        """
        Adds a vertex to the graph

        Args:
            vertex (T): Name of the vertex to add
        """
        raise NotImplementedError()

    def remove_vertex(self, vertex: Vertex) -> None:
        """
        Removes a vertex from the graph as well as edges connected to it

        Args:
            vertex (T): Name of the vertex to remove
        """
        raise NotImplementedError()

    def add_edge(self, src: Vertex, dest: Vertex) -> None:
        """
        Adds an edge connecting two vertices. Also adds the vertices if they
        don't exist in the graph

        Agrs:
            src (T): Name of the source vertex
            dest (T): Name of the destination vertex
        """
        raise NotImplementedError()

    def remove_edge(self, src: Vertex, dest: Vertex) -> None:
        """
        Removes an edge connecting two vertices

        Args:
            src (T): Name of the source vertex
            dest (T): Name of the destination vertex
        """
        raise NotImplementedError()

    def get_neighbours(self, vertex: Vertex) -> Set[Vertex]:
        """
        Gets connected vertices of a single vertex

        Args:
            vertex (T): Name of vertex

        Returns:
            Set of connected vertices
        """
        raise NotImplementedError()

    def get_edges(self, vertex: Vertex) -> Set[Edge]:
        """
        Gets all edges connected to a vertex

        Args:
            vertex (T): Name of vertex

        Returns:
            Set of tuples as edges
        """

    def are_adjacent(self, a: Vertex, b: Vertex) -> bool:
        """
        Checks if two vertices are adjacent

        Args:
            a (T): Name of the first vertex
            b (T): Name of the second vertex
        """
        raise NotImplementedError()
