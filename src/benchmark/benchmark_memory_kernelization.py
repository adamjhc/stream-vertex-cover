import sys

sys.path.append("../local")
sys.path.append("../local_stream")

from local_kernel import vertex_cover_kernelization
from local_stream import _kernelize
import networkx as nx


@profile
def profile_stream_kernelization(graph_name: str, k: int):
    _kernelize(f"../test_sets/labelled_edge_lists/{graph_name}_labelled.txt", k)


@profile
def profile_local_kernelization(graph_name: str, k: int):
    graph = nx.read_edgelist(f"../test_sets/edge_lists/{graph_name}.txt")
    vertex_cover_kernelization(graph, k)


if __name__ == "__main__":
    graph_name = "high_node_low_vc_100_10000_shuffled"
    k = 112
    profile_stream_kernelization(graph_name, k)
    profile_local_kernelization(graph_name, k)
