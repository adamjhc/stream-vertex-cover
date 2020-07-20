import sys

sys.path.append("../local")
sys.path.append("../local_stream")

from typing import List

import networkx as nx
import pyperf

from local_stream import _calculate_vertex_cover
from local_branching import vertex_cover_branching


def benchmark_branching():
    runner = pyperf.Runner()
    labelled_graph_path = "../test_sets/labelled_edge_lists/{}_labelled.txt"
    graphs: List[str] = [
        "connected_star_graph_6_10",
        "connected_star_graph_7_15",
        "florentine_families",
        "high_node_low_vc_10_1000_shuffled",
        "karate_club",
        "petersen",
    ]

    for graph_name in graphs:
        # Get number of nodes in graph
        filename = labelled_graph_path.format(graph_name)
        with open(filename) as stream:
            graph_nodes = int(stream.readline().split()[0])

        # Generate k values up to graph nodes to test with
        k_values = []
        for i in range(1, graph_nodes):
            if 2 ** i < graph_nodes and i <= 4:
                k_values.append(2 ** i)
            else:
                break

        for k in k_values:
            runner.bench_func(
                f"local-{graph_name}-{k}", benchmark_local_branching, graph_name, k,
            )
            runner.bench_func(
                f"stream-{graph_name}-{k}", benchmark_stream_branching, graph_name, k,
            )


def benchmark_local_branching(graph_name: str, k: int):
    graph = nx.read_edgelist(f"../test_sets/edge_lists/{graph_name}.txt")
    vertex_cover_branching(graph, k)


def benchmark_stream_branching(graph_name: str, k: int):
    _calculate_vertex_cover(
        f"../test_sets/labelled_edge_lists/{graph_name}_labelled.txt", k
    )


if __name__ == "__main__":
    benchmark_branching()
