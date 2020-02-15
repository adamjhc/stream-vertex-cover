"""Usage: kernel_stream_demo.py <edge_list_file> <k> [--delay=DELAY --label]

Demonstration of the kernelization of a graph edgelist

Arguments:
    edge_list_file      Path to a graph in the form of an edge list
    k                   Size up to which to generate a kernel for

Options:
    -h --help           Show this screen
    --delay=DELAY       Specify delay between iterations [default: 0.5]
    --label             Show labels in animation
"""
import sys
from typing import Any, Dict

import matplotlib.pyplot as plot
import networkx as nx
from docopt import docopt


def kernel_stream_demo(arguments: Dict[str, Any]):
    # Check whether given edgelist is weighted
    read_func = nx.read_edgelist
    with open(arguments["<edge_list_file>"], "r") as edgelist:
        line = edgelist.readline()
        if len(line.split()) > 2:
            read_func = nx.read_weighted_edgelist

    # Set up graphs
    graph = read_func(arguments["<edge_list_file>"])
    k = int(arguments["<k>"])
    kernel = nx.Graph()
    no_in_matching = 0
    maximal_matching = set()

    # Set up matplotlib
    layout = nx.spring_layout(graph)
    plot.show()

    for i, (u, v) in enumerate(list(graph.edges)):

        print("{:10} {}".format(u, v))

        # Kernelization algorithm
        is_neighbour = False
        if _in(u, maximal_matching) and kernel.degree[u] < k:
            kernel.add_edge(u, v)
            is_neighbour = True

        if _in(v, maximal_matching) and kernel.degree[v] < k:
            kernel.add_edge(u, v)
            is_neighbour = True

        if not is_neighbour:
            no_in_matching += 1
            maximal_matching.add((u, v))
            kernel.add_edge(u, v)

            if no_in_matching > k:
                print("There is no such kernel of size", k)
                break

        # matplotlib updates
        plot.clf()
        plot.title(f"Iteration {i}")

        # Red colour for nodes in the matching
        node_colours = [
            "r" if _in(node, maximal_matching) else "#1f78b4" for node in kernel.nodes
        ]

        # Red colour for edges between two matched nodes
        edge_colours = [
            "r" if (u, v) in maximal_matching else "k" for u, v in kernel.edges
        ]

        nx.draw(
            kernel,
            pos=layout,
            with_labels=arguments["--label"],
            node_color=node_colours,
            edge_color=edge_colours,
        )
        plot.pause(float(arguments["--delay"]))

    print("Finished")
    plot.show()


def _in(item, pairs):
    for pair in pairs:
        if item in pair:
            return True

    return False


if __name__ == "__main__":
    arguments = docopt(__doc__)
    kernel_stream_demo(arguments)
