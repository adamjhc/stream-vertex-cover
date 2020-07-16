"""Usage: generate_high_node_low_vc_graph.py <core_count> <neighbours>

Arguments:
    core_count      Number of highly connected nodes
    neighbours      Number of neighbours to highly connected nodes

Options:
    --help -h       Show this screen
"""
import random

from docopt import docopt
from networkx import Graph, write_edgelist


def generate_high_node_low_vc_graph(core_count: int, neighbours: int):
    graph = Graph()

    cores = list(range(0, core_count * neighbours, neighbours + 1))

    # generate star graphs
    for i in cores:
        for j in range(i + 1, i + 1 + neighbours):
            graph.add_edge(i, j)

    # randomly connect stars together
    for i in cores:
        random_choice = i
        while random_choice == i:
            random_choice = random.choice(cores)
        graph.add_edge(i, random_choice)

    write_edgelist(
        graph, f"high_node_low_vc_{core_count}_{neighbours}.txt", data=False,
    )


if __name__ == "__main__":
    args = docopt(__doc__)
    generate_high_node_low_vc_graph(
        int(args["<core_count>"]), int(args["<neighbours>"])
    )
