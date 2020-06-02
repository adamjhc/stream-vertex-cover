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
from typing import Any, Dict, Set, Tuple

import matplotlib.pyplot as plot
import networkx as nx
from docopt import docopt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.legend_handler import HandlerLine2D
from matplotlib.lines import Line2D

from visuals_util import _in, get_graph_layout, get_read_func_from_edgelist


def kernel_stream_demo(args: Dict[str, Any]):
    path = args["<edge_list_file>"]
    read_func = get_read_func_from_edgelist(path)

    # Set up graphs
    graph = read_func(path)
    edges = list(graph.edges)
    k = int(args["<k>"])
    kernel = nx.Graph()
    no_in_matching = 0
    maximal_matching: Set[Tuple[Any, Any]] = set()

    # Set up matplotlib
    layout = get_graph_layout(graph)

    # Build plot
    plot.show()

    for i, (u, v) in enumerate(edges):

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

        ax_left: Axes = plot.subplot(1, 2, 1)
        ax_left.set_title(f"Kernel - Iteration {i}")
        ax_left.legend(
            handles=[
                Line2D([0], [0], label=node_type, color=node_colour, marker="o")
                for node_type, node_colour in zip(node_type_names, node_type_colours)
            ],
            handler_map={Line2D: HandlerLine2D(numpoints=2)},
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
            ax=ax_left,
            pos=layout,
            with_labels=args["--label"],
            node_color=node_colours,
            node_size=node_sizes,
            edge_color=edge_colours,
            width=edge_widths,
        )

        # Right subplot - showing entire graph
        ax_right: Axes = plot.subplot(1, 2, 2)
        ax_right.set_title("Entire graph")

        node_type_names = ["Current", "In Kernel", "Not in Kernel"]
        node_type_colours = ["y", "m", "k"]

        ax_right.legend(
            handles=[
                Line2D([0], [0], label=node_type, color=node_colour, marker="o")
                for node_type, node_colour in zip(node_type_names, node_type_colours)
            ],
            handler_map={Line2D: HandlerLine2D(numpoints=2)},
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
            ax=ax_right,
            pos=layout,
            with_labels=args["--label"],
            node_color=node_colours,
            node_size=50,
            edge_color=edge_colours,
        )

        # Wait for update
        plot.pause(float(args["--delay"]))

    print("Finished")
    plot.show()


if __name__ == "__main__":
    args = docopt(__doc__)
    kernel_stream_demo(args)
