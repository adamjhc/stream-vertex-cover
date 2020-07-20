import sys

sys.path.append("../local")
sys.path.append("../local_stream")

from typing import List

import networkx as nx
import pyperf

from local_kernel import vertex_cover_kernelization
from local_stream import _kernelize


def benchmark_kernelization():
    runner = pyperf.Runner()
    labelled_graph_path = "../test_sets/labelled_edge_lists/{}_labelled.txt"
    graphs: List[str] = [
        "connected_star_graph_6_10",
        "connected_star_graph_7_15",
        "erdos_renyi_100_0.3_edgelist",
        "erdos_renyi_100_0.4_edgelist",
        "erdos_renyi_100_0.5_edgelist",
        "erdos_renyi_100_0.05_edgelist",
        "erdos_renyi_100_0.6_edgelist",
        "erdos_renyi_100_0.7_edgelist",
        "erdos_renyi_100_0.07_edgelist",
        "erdos_renyi_100_0.8_edgelist",
        "erdos_renyi_100_0.9_edgelist",
        "erdos_renyi_100_0.09_edgelist",
        "erdos_renyi_100_0.11_edgelist",
        "erdos_renyi_100_0.13_edgelist",
        "erdos_renyi_100_0.15_edgelist",
        "erdos_renyi_100_0.17_edgelist",
        "erdos_renyi_100_0.19_edgelist",
        "erdos_renyi_100_0.21_edgelist",
        "erdos_renyi_100_0.23_edgelist",
        "erdos_renyi_100_0.25_edgelist",
        "erdos_renyi_100_0.27_edgelist",
        "erdos_renyi_100_0.35_edgelist",
        "erdos_renyi_100_0.45_edgelist",
        "erdos_renyi_100_0.55_edgelist",
        "erdos_renyi_100_0.65_edgelist",
        "erdos_renyi_100_0.75_edgelist",
        "erdos_renyi_100_0.85_edgelist",
        "erdos_renyi_100_0.95_edgelist",
        "erdos_renyi_100_1.0_edgelist",
        "florentine_families",
        "high_node_low_vc_10_1000_shuffled",
        "high_node_low_vc_10_10000_shuffled",
        # "high_node_low_vc_10_100000_shuffled",
        "high_node_low_vc_50_100_shuffled",
        "high_node_low_vc_50_1000_shuffled",
        # "high_node_low_vc_50_10000_shuffled",
        # "high_node_low_vc_50_50000_shuffled",
        "high_node_low_vc_100_1000_shuffled",
        # "high_node_low_vc_100_10000_shuffled",
        "karate_club",
        "les_miserables",
        "petersen",
        "tutte",
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
                f"local-{graph_name}-{k}", benchmark_local_kernelization, graph_name, k,
            )
            runner.bench_func(
                f"stream-{graph_name}-{k}",
                benchmark_stream_kernelization,
                graph_name,
                k,
            )


def benchmark_local_kernelization(graph_name: str, k: int):
    graph = nx.read_edgelist(f"../test_sets/edge_lists/{graph_name}.txt")
    vertex_cover_kernelization(graph, k)


def benchmark_stream_kernelization(graph_name: str, k: int):
    _kernelize(f"../test_sets/labelled_edge_lists/{graph_name}_labelled.txt", k)


if __name__ == "__main__":
    benchmark_kernelization()
