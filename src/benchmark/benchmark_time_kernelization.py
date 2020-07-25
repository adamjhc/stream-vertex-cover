import sys

sys.path.append("../local")
sys.path.append("../local_stream")

from typing import List, Dict

import networkx as nx
import pyperf

from local_kernel import _kernelize as local_kernelize
from local_stream import _kernelize as stream_kernelize


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
                    benchmark_local_kernelization,
                    graph_name,
                    k,
                )
                runner.bench_func(
                    f"stream-{graph_name}-{edges}-{k}",
                    benchmark_stream_kernelization,
                    graph_name,
                    k,
                )


def benchmark_local_kernelization(graph_name: str, k: int):
    graph = nx.read_edgelist(f"../test_sets/edge_lists/{graph_name}.txt")
    kernel, vertex_cover = local_kernelize(graph, k)

    if kernel.number_of_edges() > k ** 2:
        return None


def benchmark_stream_kernelization(graph_name: str, k: int):
    stream_kernelize(f"../test_sets/labelled_edge_lists/{graph_name}_labelled.txt", k)


if __name__ == "__main__":
    benchmark_kernelization()
