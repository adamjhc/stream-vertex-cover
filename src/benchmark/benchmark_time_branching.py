import sys

sys.path.append("../local")
sys.path.append("../local_stream")

from typing import List, Dict

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
        "high_node_low_vc_10_10000_shuffled",
        "karate_club",
        "petersen",
    ]

    # Generate k values up to graph nodes to test with
    k_values_for_graphs: Dict[str, List[int]] = {}
    graph_edges_for_graphs: Dict[str, int] = {}
    for graph_name in graphs:
        # Get number of nodes in graph
        filename = labelled_graph_path.format(graph_name)
        with open(filename) as stream:
            graph_label = stream.readline().split()[:2]
            graph_nodes = int(graph_label[0])
            graph_edges = int(graph_label[1])
            graph_edges_for_graphs[graph_name] = graph_edges

        k_values_for_graphs[graph_name] = []
        for i in range(1, graph_nodes):
            if 2 ** (i - 1) < graph_nodes:
                k_values_for_graphs[graph_name].append(2 ** i)
            else:
                break

    for i in range(len(max(k_values_for_graphs.values()))):
        for graph_name in graphs:
            if i < len(k_values_for_graphs[graph_name]):
                k = k_values_for_graphs[graph_name][i]
                edges = graph_edges_for_graphs[graph_name]
                runner.bench_func(
                    f"local-{graph_name}-{edges}-{k}",
                    benchmark_local_branching,
                    graph_name,
                    k,
                )
                runner.bench_func(
                    f"stream-{graph_name}-{edges}-{k}",
                    benchmark_stream_branching,
                    graph_name,
                    k,
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
