"""Usage: kernel_stream_demo.py <edge_list_file> <k> [--delay=DELAY --label]

Demonstration of the kernelization of a graph edgelist

Arguments:
    edge_list_file      Path to a graph in the form of an edge list
    k                   Size up to which to generate a kernel for

Options:
    -h --help           Show this screen
    --delay=DELAY       Specify delay between iterations [default: 0.5]
    --label             Show labels on nodes
"""
import sys
from typing import Any, Dict

import matplotlib.pyplot as plot
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
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
    layout = None
    if graph.number_of_edges() < 1000:
        layout = nx.kamada_kawai_layout(graph)
    else:
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

        # Left subplot - showing kernel
        node_type_names = ["Matched", "Neighbour"]
        node_type_colours = ["r", "k"]

        ax1: Axes = plot.subplot(1, 2, 1)
        ax1.set_title(f"Kernel - Iteration {i}")
        ax1.legend(
            handles=[
                Line2D(
                    [0], [0], color=node_type_colours[i], label=node_type, marker="o"
                )
                for i, node_type in enumerate(node_type_names)
            ],
            loc="lower right",
        )

        node_colours = [
            node_type_colours[0]
            if _in(node, maximal_matching)
            else node_type_colours[1]
            for node in kernel.nodes
        ]

        edge_colours = [
            node_type_colours[0] if edge in maximal_matching else node_type_colours[1]
            for edge in kernel.edges
        ]

        # Smaller node for nodes not in the matching
        node_sizes = [
            250 if _in(node, maximal_matching) else 50 for node in kernel.nodes
        ]

        # Thicker edge for edges between edges in matching
        edge_widths = [2 if edge in maximal_matching else 0.5 for edge in kernel.edges]

        nx.draw(
            kernel,
            ax=ax1,
            pos=layout,
            with_labels=arguments["--label"],
            node_color=node_colours,
            node_size=node_sizes,
            edge_color=edge_colours,
            width=edge_widths,
        )

        # Right subplot - showing entire graph
        ax2: Axes = plot.subplot(1, 2, 2)
        ax2.set_title("Entire graph")

        node_type_names = ["Current", "In Kernel", "Not in Kernel"]
        node_type_colours = ["y", "m", "k"]

        ax2.legend(
            handles=[
                Line2D(
                    [0], [0], color=node_type_colours[i], label=node_type, marker="o"
                )
                for i, node_type in enumerate(node_type_names)
            ],
            loc="lower right",
        )

        node_colours = [
            node_type_colours[0]
            if node in (u, v)
            else node_type_colours[1]
            if node in kernel.nodes
            else node_type_colours[2]
            for node in graph.nodes
        ]

        edge_colours = [
            node_type_colours[0]
            if edge == (u, v)
            else node_type_colours[1]
            if edge in kernel.edges
            else node_type_colours[2]
            for edge in graph.edges
        ]

        nx.draw(
            graph,
            ax=ax2,
            pos=layout,
            with_labels=arguments["--label"],
            node_color=node_colours,
            node_size=50,
            edge_color=edge_colours,
        )

        # Wait for update
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
