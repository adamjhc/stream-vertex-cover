from pytest import fixture

from src.graph_adjacency_list import AdjacencyListGraph


@fixture
def graph():
    # Set Up
    graph = {
        "a": ["d"],
        "b": ["c"],
        "c": ["b", "c", "d", "e"],
        "d": ["a", "c"],
        "e": ["c"],
        "f": [],
    }

    # Pass
    yield AdjacencyListGraph(graph)

    # Tear Down


def test_add_vertex(graph):
    # arrange
    vertex = "g"

    # act
    graph.add_vertex(vertex)

    # assert
    assert vertex in graph.vertices()


def test_add_edge(graph):
    # arrange
    vertexA = "a"
    vertexB = "b"

    # act
    graph.add_edge(vertexA, vertexB)

    # assert
    assert vertexA in graph._AdjacencyListGraph__graph[vertexB]
    assert vertexB in graph._AdjacencyListGraph__graph[vertexA]
    assert (vertexA, vertexB) in graph.edges()
