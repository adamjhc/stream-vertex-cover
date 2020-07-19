import sys

sys.path.append("../local_stream")

from typing import List

import networkx as nx
import pyperf

from local_stream import _calculate_vertex_cover


def benchmark_time_branching():
    graph_path = "../test_sets/labelled_edge_lists/{}.txt"

    runner = pyperf.Runner()
    graphs: List[str] = [
        "connected_star_graph_6_10_labelled",
        "connected_star_graph_7_15_labelled",
        # "erdos_renyi_100_0.3_edgelist_labelled",
        # "erdos_renyi_100_0.4_edgelist_labelled",
        # "erdos_renyi_100_0.5_edgelist_labelled",
        # "erdos_renyi_100_0.05_edgelist_labelled",
        # "erdos_renyi_100_0.6_edgelist_labelled",
        # "erdos_renyi_100_0.7_edgelist_labelled",
        # "erdos_renyi_100_0.07_edgelist_labelled",
        # "erdos_renyi_100_0.8_edgelist_labelled",
        # "erdos_renyi_100_0.9_edgelist_labelled",
        # "erdos_renyi_100_0.09_edgelist_labelled",
        # "erdos_renyi_100_0.11_edgelist_labelled",
        # "erdos_renyi_100_0.13_edgelist_labelled",
        # "erdos_renyi_100_0.15_edgelist_labelled",
        # "erdos_renyi_100_0.17_edgelist_labelled",
        # "erdos_renyi_100_0.19_edgelist_labelled",
        # "erdos_renyi_100_0.21_edgelist_labelled",
        # "erdos_renyi_100_0.23_edgelist_labelled",
        # "erdos_renyi_100_0.25_edgelist_labelled",
        # "erdos_renyi_100_0.27_edgelist_labelled",
        # "erdos_renyi_100_0.35_edgelist_labelled",
        # "erdos_renyi_100_0.45_edgelist_labelled",
        # "erdos_renyi_100_0.55_edgelist_labelled",
        # "erdos_renyi_100_0.65_edgelist_labelled",
        # "erdos_renyi_100_0.75_edgelist_labelled",
        # "erdos_renyi_100_0.85_edgelist_labelled",
        # "erdos_renyi_100_0.95_edgelist_labelled",
        # "erdos_renyi_100_1.0_edgelist_labelled",
        "florentine_families_labelled",
        "high_node_low_vc_10_1000_shuffled_labelled",
        "high_node_low_vc_10_10000_shuffled_labelled",
        "high_node_low_vc_10_100000_shuffled_labelled",
        # "high_node_low_vc_50_100_shuffled_labelled",
        # "high_node_low_vc_50_1000_shuffled_labelled",
        # "high_node_low_vc_50_10000_shuffled_labelled",
        # "high_node_low_vc_50_50000_shuffled_labelled",
        # "high_node_low_vc_100_1000_shuffled_labelled",
        # "high_node_low_vc_100_10000_shuffled_labelled",
        "karate_club_labelled",
        # "les_miserables_labelled",
        "petersen_labelled",
        # "tutte_labelled",
    ]

    for graph_name in graphs:
        filename = graph_path.format(graph_name)
        with open(filename) as stream:
            graph_nodes = int(stream.readline().split()[0])

        exponents = []
        for i in range(1, graph_nodes):
            if 2 ** i < graph_nodes:
                exponents.append(i)
            else:
                break

        for exp in exponents:
            runner.bench_func(
                f"{graph_name}-{2 ** exp}", _calculate_vertex_cover, filename, 2 ** exp
            )


if __name__ == "__main__":
    benchmark_time_branching()
