from src.graph import Graph


class AdjacencyMatrixDictGraph(Graph):
    """
    Adjacency Matrix implementation of a Graph using dictionaries
    """

    def __init__(self):
        self.graph = dict()

    def __repr__(self):
        return repr(self.graph)

    def add_vertex(self, vertex):
        """
        Adds a vertex to the graph

        Args:
            vertex (str): Name of the vertex to add
        """
        if not vertex in self.graph:
            self.graph[vertex] = dict()

    def remove_vertex(self, vertex):
        """
        Removes a vertex from the graph as well as edges connected to it

        Args:
            vertex (str): Name of the vertex to remove
        """
        if vertex in self.graph:
            # Remove vertex connection from other vertices
            for v in self.graph[vertex]:
                self.graph[v].pop(vertex)

            self.graph.pop(vertex)

    def add_edge(self, src, dest):
        """
        Adds an edge connecting two vertices

        Agrs:
            src (str): Name of the source vertex
            dest (str): Name of the destination vertex
        """
        self.add_vertex(src)
        self.add_vertex(dest)

        self.graph[src][dest] = 1
        self.graph[dest][src] = 1

    def remove_edge(self, src, dest):
        """
        Removes an edge connecting two vertices

        Args:
            src (str): Name of the source vertex
            dest (str): Name of the destination vertex
        """
        if src in self.graph and dest in self.graph:
            self.graph[src][dest] = 0
            self.graph[dest][src] = 0

    def areAdjacent(self, a, b):
        """
        Checks if two vertices are adjacent

        Args:
            a (str): Name of the first vertex
            b (str): Name of the second vertex
        """
        return self.graph[a][b] == 1


class AdjacencyMatrixListGraph(Graph):
    """
    Adjacency Matrix implementation of a Graph using lists
    """

    def __init__(self):
        self.graph = []

    def __repr__(self):
        return repr(self.graph)

    def add_vertex(self, vertex):
        """
        Adds a vertex to the graph

        Args:
            vertex (int): Name of the vertex to add
        """
        if not vertex in self.graph:
            self.graph.append(vertex)
            self.graph[vertex] = []

    def remove_vertex(self, vertex):
        """
        Removes a vertex from the graph as well as edges connected to it

        Args:
            vertex (int): Name of the vertex to remove
        """
        if vertex in self.graph:
            # Remove vertex connection from other vertices
            for v in self.graph[vertex]:
                self.graph[v].remove(vertex)

            self.graph.remove(vertex)

    def add_edge(self, src, dest):
        """
        Adds an edge connecting two vertices

        Agrs:
            src (str): Name of the source vertex
            dest (str): Name of the destination vertex
        """
        if not src in self.graph:
            self.graph[src] = []
        if not dest in self.graph:
            self.graph[dest] = []

        self.graph[src][dest] = 1
        self.graph[dest][src] = 1

    def remove_edge(self, src, dest):
        """
        Removes an edge connecting two vertices

        Args:
            src (str): Name of the source vertex
            dest (str): Name of the destination vertex
        """
        if src in self.graph and dest in self.graph:
            self.graph[src][dest] = 0
            self.graph[dest][src] = 0

    def areAdjacent(self, a, b):
        """
        Checks if two vertices are adjacent

        Args:
            a (str): Name of the first vertex
            b (str): Name of the second vertex
        """
        return self.graph[a][b] == 1