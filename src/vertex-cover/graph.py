class Graph(object):
    """
    Graph Interface
    """

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
        Adds an edge connecting two vertices

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

