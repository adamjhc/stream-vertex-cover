from src.graph import Graph


class AdjacencyListGraph(Graph):
    """
    Adjacency List implementation of a Graph
    """

    def __init__(self, graph=None):
        """
        Initialises the graph with the option to pass in an existing graph
        """
        if graph == None:
            graph = dict()
        self.__graph = dict()

    def __repr__(self):
        """
        Returns:
            Printable representation of the graph
        """
        return repr(self.__graph)

    def vertices(self):
        """
        Returns:
            List of vertices in the graph
        """
        return self.__graph.keys()

    def edges(self):
        """
        Returns:
            List of all edges as pairs in the graph
        """
        edges = []
        for vertex in self.__graph:
            for connected in self.__graph:
                edges.append((vertex, connected))

        return edges

    def add_vertex(self, vertex):
        """
        Adds a vertex to the graph

        Args:
            vertex (str): Name of the vertex to add
        """
        if vertex not in self.__graph:
            self.__graph[vertex] = set()

    def remove_vertex(self, vertex):
        """
        Removes a vertex from the graph as well as edges connected to it

        Args:
            vertex (str): Name of the vertex to remove
        """
        if vertex in self.__graph:
            # Remove vertex connection from other vertices
            for v in self.__graph[vertex]:
                self.__graph[v].remove(vertex)

            self.__graph.pop(vertex)

    def add_edge(self, src, dest):
        """
        Adds an edge connecting two vertices. Also adds the vertices if they
        don't exist in the graph

        Agrs:
            src (str): Name of the source vertex
            dest (str): Name of the destination vertex
        """
        self.add_vertex(src)
        self.add_vertex(dest)

        self.__graph[src].add(dest)
        self.__graph[dest].add(src)

    def remove_edge(self, src, dest):
        """
        Removes an edge connecting two vertices

        Args:
            src (str): Name of the source vertex
            dest (str): Name of the destination vertex
        """
        if src in self.__graph and dest in self.__graph:
            if src in self.__graph[dest] and dest in self.__graph[src]:
                self.__graph[src].remove(dest)
                self.__graph[dest].remove(src)

    def areAdjacent(self, a, b):
        """
        Checks if two vertices are adjacent

        Args:
            a (str): Name of the first vertex
            b (str): Name of the second vertex

        Returns:
            True if two vertices are adjacent, False if not
        """
        return b in self.__graph[a]
