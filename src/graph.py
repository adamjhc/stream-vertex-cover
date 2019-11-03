class Graph(object):
    """
    Graph Interface
    """

    def vertices(self):
        """
        Returns:
            List of vertices in the graph
        """
        raise NotImplementedError()

    def edges(self):
        """
        Returns:
            List of all edges as pairs in the graph
        """
        raise NotImplementedError()

    def add_vertex(self, vertex):
        """
        Adds a vertex to the graph

        Args:
            vertex (str): Name of the vertex to add
        """
        raise NotImplementedError()

    def remove_vertex(self, vertex):
        """
        Removes a vertex from the graph as well as edges connected to it

        Args:
            vertex (str): Name of the vertex to remove
        """
        raise NotImplementedError()

    def add_edge(self, src, dest):
        """
        Adds an edge connecting two vertices. Also adds the vertices if they
        don't exist in the graph

        Agrs:
            src (str): Name of the source vertex
            dest (str): Name of the destination vertex
        """
        raise NotImplementedError()

    def remove_edge(self, src, dest):
        """
        Removes an edge connecting two vertices

        Args:
            src (str): Name of the source vertex
            dest (str): Name of the destination vertex
        """
        raise NotImplementedError()

    def areAdjacent(self, a, b):
        """
        Checks if two vertices are adjacent

        Args:
            a (str): Name of the first vertex
            b (str): Name of the second vertex
        """
        raise NotImplementedError()
