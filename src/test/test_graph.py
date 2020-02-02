from pytest import fixture

from src.graph import (
    AdjacencyListGraph,
    # AdjacencyMatrixDictGraph,
    # AdjacencyMatrixListGraph,
)


@fixture(
    params=[
        AdjacencyListGraph,
        # AdjacencyMatrixDictGraph,
        # AdjacencyMatrixListGraph
    ]
)
def Implementation(request):
    return request.param


def test_add_vertex(Implementation):
    # arrange
    graph = Implementation()
    vertex = "g"

    # act
    graph.add_vertex(vertex)

    # assert
    assert vertex in graph.vertices()


def test_remove_vertex(Implementation):
    pass


def test_add_edge(Implementation):
    # arrange
    graph = Implementation()
    vertexA = "a"
    vertexB = "b"

    # act
    graph.add_edge(vertexA, vertexB)

    # assert
    assert vertexA in graph._AdjacencyListGraph__graph[vertexB]
    assert vertexB in graph._AdjacencyListGraph__graph[vertexA]
    assert (vertexA, vertexB) in graph.edges()


def test_remove_edge(Implementation):
    assert True


def test_vertices(Implementation):
    assert True


def test_edges(Implementation):
    assert True


def test_get_neighbours(Implementation):
    assert True


def test_are_adjacent(Implementation):
    assert True
