from typing import TypeVar

from .graph_interface import Graph

Vertex = TypeVar("Vertex")


class AdjacencyMatrixListGraph(Graph[Vertex]):
    """
    Adjacency Matrix implementation of a Graph using lists
    """

    def __init__(self):
        self.graph = []

    def __repr__(self):
        return repr(self.graph)

    def add_vertex(self, vertex: Vertex):
        """
        Adds a vertex to the graph

        Args:
            vertex (int): Name of the vertex to add
        """
        if not vertex in self.graph:
            self.graph.append(vertex)
            self.graph[vertex] = []

    def remove_vertex(self, vertex: Vertex):
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

    def add_edge(self, src: Vertex, dest: Vertex):
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

    def remove_edge(self, src: Vertex, dest: Vertex):
        """
        Removes an edge connecting two vertices

        Args:
            src (str): Name of the source vertex
            dest (str): Name of the destination vertex
        """
        if src in self.graph and dest in self.graph:
            self.graph[src][dest] = 0
            self.graph[dest][src] = 0

    def areAdjacent(self, a: Vertex, b: Vertex):
        """
        Checks if two vertices are adjacent

        Args:
            a (str): Name of the first vertex
            b (str): Name of the second vertex
        """
        return self.graph[a][b] == 1
