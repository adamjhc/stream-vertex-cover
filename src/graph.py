from typing import TypeVar, Generic

T = TypeVar("T")


class Graph(Generic[T]):
    """
    Graph Interface
    """

    def vertices(self) -> set[T]:
        """
        Returns:
            Set of vertices in the graph
        """
        raise NotImplementedError()

    def edges(self) -> set[()]:
        """
        Returns:
            Set of all edges as pairs in the graph
        """
        raise NotImplementedError()

    def add_vertex(self, vertex: T) -> None:
        """
        Adds a vertex to the graph

        Args:
            vertex (T): Name of the vertex to add
        """
        raise NotImplementedError()

    def remove_vertex(self, vertex: T) -> None:
        """
        Removes a vertex from the graph as well as edges connected to it

        Args:
            vertex (T): Name of the vertex to remove
        """
        raise NotImplementedError()

    def add_edge(self, src: T, dest: T) -> None:
        """
        Adds an edge connecting two vertices. Also adds the vertices if they
        don't exist in the graph

        Agrs:
            src (T): Name of the source vertex
            dest (T): Name of the destination vertex
        """
        raise NotImplementedError()

    def remove_edge(self, src: T, dest: T) -> None:
        """
        Removes an edge connecting two vertices

        Args:
            src (T): Name of the source vertex
            dest (T): Name of the destination vertex
        """
        raise NotImplementedError()

    def get_neighbours(self, vertex: T) -> set[T]:
        """
        Gets connected vertices of a single vertex

        Args:
            vertex (T): Name of vertex

        Returns:
            Set of connected vertices
        """
        raise NotImplementedError()

    def get_edges(self, vertex: T) -> set[()]:
        """
        Gets all edges connected to a vertex

        Args:
            vertex (T): Name of vertex

        Returns:
            Set of tuples as edges
        """

    def are_adjacent(self, a: T, b: T) -> bool:
        """
        Checks if two vertices are adjacent

        Args:
            a (T): Name of the first vertex
            b (T): Name of the second vertex
        """
        raise NotImplementedError()
