import sys

sys.path.append("../local")
sys.path.append("../local_stream")

from local_branching import vertex_cover_branching
from local_stream import branching
import networkx as nx


@profile
def profile_stream_branching(graph_name: str, k: int):
    branching(f"../test_sets/labelled_edge_lists/{graph_name}_labelled.txt", k)


@profile
def profile_local_branching(graph_name: str, k: int):
    graph = nx.read_edgelist(f"../test_sets/edge_lists/{graph_name}.txt")
    vertex_cover_branching(graph, k)


if __name__ == "__main__":
    graph_name = "high_node_low_vc_10_100000_shuffled"
    k = 12
    profile_stream_branching(graph_name, k)
    profile_local_branching(graph_name, k)
