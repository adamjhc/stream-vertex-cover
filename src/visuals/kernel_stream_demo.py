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
    kernel_exists = True
    graph = read_func(path)
    edges = list(graph.edges)
    k = int(args["<k>"])
    kernel = nx.Graph()
    no_in_matching = 0
    maximal_matching: Set[Tuple[Any, Any]] = set()

    # Set up matplotlib
    plot.show()
    figure: Figure = plot.figure("Kernelization Algorithm", figsize=(16, 9))
    figure.suptitle("Kernelization Algorithm")
    layout = get_graph_layout(graph)
    delay = float(args["--delay"])
    with_labels = args["--label"]

    ## Left subplot - kernel
    left_axes: Axes = figure.add_subplot(1, 2, 1)
    left_node_type_names = ["Matched", "Neighbour"]
    left_node_type_colours = ["r", "k"]
    left_node_type_sizes = [250, 50]
    left_edge_type_widths = [2, 0.5]

    ## Right subplot - whole graph
    right_axes: Axes = figure.add_subplot(1, 2, 2)
    right_node_type_names = ["Current", "In Kernel", "Not in Kernel"]
    right_node_type_colours = ["y", "m", "k"]

    for i, (u, v) in enumerate(edges):
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
                figure.text(
                    0.5,
                    0.05,
                    f"There is no such kernel of size {k}",
                    fontsize=24,
                    horizontalalignment="center",
                    verticalalignment="center",
                    transform=figure.transFigure,
                )
                kernel_exists = False
                break

        # matplotlib updates
        left_axes.clear()
        right_axes.clear()

        ## Left subplot - kernel
        left_axes.set_title(f"Kernel - Iteration {i}")
        left_axes.legend(
            handles=[
                Line2D([0], [0], label=node_type, color=node_colour, marker="o")
                for node_type, node_colour in zip(
                    left_node_type_names, left_node_type_colours
                )
            ],
            handler_map={Line2D: HandlerLine2D(numpoints=2)},
            loc="lower right",
        )

        left_node_colours = []
        left_node_sizes = []
        for node in kernel.nodes:
            node_type = 0 if _in(node, maximal_matching) else 1

            left_node_colours.append(left_node_type_colours[node_type])
            left_node_sizes.append(left_node_type_sizes[node_type])

        left_edge_colours = []
        left_edge_widths = []
        for edge in kernel.edges:
            edge_type = 0 if edge in maximal_matching else 1

            left_edge_colours.append(left_node_type_colours[edge_type])
            left_edge_widths.append(left_edge_type_widths[edge_type])

        nx.draw(
            kernel,
            ax=left_axes,
            pos=layout,
            with_labels=with_labels,
            node_color=left_node_colours,
            node_size=left_node_sizes,
            edge_color=left_edge_colours,
            width=left_edge_widths,
        )

        ## Right subplot - showing entire graph
        right_axes.set_title("Entire graph")
        right_axes.legend(
            handles=[
                Line2D([0], [0], label=node_type, color=node_colour, marker="o")
                for node_type, node_colour in zip(
                    right_node_type_names, right_node_type_colours
                )
            ],
            handler_map={Line2D: HandlerLine2D(numpoints=2)},
            loc="lower right",
        )

        right_node_colours = [
            right_node_type_colours[0]
            if node in (u, v)
            else right_node_type_colours[1]
            if node in kernel.nodes
            else right_node_type_colours[2]
            for node in graph.nodes
        ]

        right_edge_colours = [
            right_node_type_colours[0]
            if edge == (u, v)
            else right_node_type_colours[1]
            if edge in kernel.edges
            else right_node_type_colours[2]
            for edge in graph.edges
        ]

        nx.draw(
            graph,
            ax=right_axes,
            pos=layout,
            with_labels=with_labels,
            node_color=right_node_colours,
            node_size=50,
            edge_color=right_edge_colours,
        )

        try:
            # Wait for update
            plot.pause(delay)
        except:
            # Exception caused when exiting
            break

    if kernel_exists:
        figure.text(
            0.5,
            0.05,
            f"A kernel exists of size {k}",
            fontsize=24,
            horizontalalignment="center",
            verticalalignment="center",
            transform=figure.transFigure,
        )
    plot.show()


if __name__ == "__main__":
    args = docopt(__doc__)
    kernel_stream_demo(args)
