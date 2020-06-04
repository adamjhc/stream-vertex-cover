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
    figure.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9)
    figure.suptitle("Kernelization Algorithm")
    layout = get_graph_layout(graph)
    delay = float(args["--delay"])
    with_labels = args["--label"]

    ## Left subplot - kernel
    kernel_axes: Axes = figure.add_subplot(1, 2, 2)
    kernel_node_type_names = ["Matched", "Neighbour"]
    kernel_node_type_colours = ["r", "k"]
    kernel_node_type_sizes = [250, 50]
    kernel_edge_type_widths = [2, 0.5]

    ## Right subplot - whole graph
    graph_axes: Axes = figure.add_subplot(1, 2, 1)
    graph_node_type_names = ["Current", "In Kernel", "Not in Kernel"]
    graph_node_type_colours = ["y", "m", "k"]

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

        kernel_no_of_nodes = kernel.number_of_nodes()
        kernel_no_of_edges = kernel.number_of_edges()
        graph_no_of_nodes = graph.number_of_nodes()
        graph_no_of_edges = graph.number_of_edges()

        # matplotlib updates
        kernel_axes.clear()
        graph_axes.clear()

        ## Left subplot - kernel
        kernel_axes.set_title(
            f"Kernel (Nodes: {kernel_no_of_nodes}, Edges: {kernel_no_of_edges}, Size of Graph: {kernel_no_of_edges/graph_no_of_edges * 100:.2f}%)"
        )
        kernel_axes.legend(
            handles=[
                Line2D([0], [0], label=node_type, color=node_colour, marker="o")
                for node_type, node_colour in zip(
                    kernel_node_type_names, kernel_node_type_colours
                )
            ],
            handler_map={Line2D: HandlerLine2D(numpoints=2)},
            loc="lower right",
        )

        kernel_node_colours = []
        kernel_node_sizes = []
        for node in kernel.nodes:
            node_type = 0 if _in(node, maximal_matching) else 1

            kernel_node_colours.append(kernel_node_type_colours[node_type])
            kernel_node_sizes.append(kernel_node_type_sizes[node_type])

        kernel_edge_colours = []
        kernel_edge_widths = []
        for edge in kernel.edges:
            edge_type = 0 if edge in maximal_matching else 1

            kernel_edge_colours.append(kernel_node_type_colours[edge_type])
            kernel_edge_widths.append(kernel_edge_type_widths[edge_type])

        nx.draw(
            kernel,
            ax=kernel_axes,
            pos=layout,
            with_labels=with_labels,
            node_color=kernel_node_colours,
            node_size=kernel_node_sizes,
            edge_color=kernel_edge_colours,
            width=kernel_edge_widths,
        )

        ## Right subplot - showing entire graph
        graph_axes.set_title(
            f"Entire graph (Nodes: {graph_no_of_nodes}, Edges: {graph_no_of_edges})"
        )
        graph_axes.legend(
            handles=[
                Line2D([0], [0], label=node_type, color=node_colour, marker="o")
                for node_type, node_colour in zip(
                    graph_node_type_names, graph_node_type_colours
                )
            ],
            handler_map={Line2D: HandlerLine2D(numpoints=2)},
            loc="lower right",
        )

        graph_node_colours = [
            graph_node_type_colours[0]
            if node in (u, v)
            else graph_node_type_colours[1]
            if node in kernel.nodes
            else graph_node_type_colours[2]
            for node in graph.nodes
        ]

        graph_edge_colours = [
            graph_node_type_colours[0]
            if edge == (u, v)
            else graph_node_type_colours[1]
            if edge in kernel.edges
            else graph_node_type_colours[2]
            for edge in graph.edges
        ]

        nx.draw(
            graph,
            ax=graph_axes,
            pos=layout,
            with_labels=with_labels,
            node_color=graph_node_colours,
            node_size=50,
            edge_color=graph_edge_colours,
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
