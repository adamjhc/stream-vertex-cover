"""Usage: kernel_stream_demo.py <edge_list_file> <k> [--delay=DELAY --label]

Demonstration of the kernelization of a graph edgelist

Arguments:
    edge_list_file      Path to a graph in the form of an edge list
    k                   Size up to which to generate a kernel for

Options:
    -h --help           Show this screen
    --delay=DELAY       Specify delay between iterations in milliseconds [default: 500]
    --label             Show labels on nodes
"""
from typing import Any, Dict, Set, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plot
import networkx as nx
from docopt import docopt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.legend_handler import HandlerLine2D
from matplotlib.lines import Line2D

from kernel_utils import draw_graph, draw_kernel
from visuals_utils import _in, get_graph_layout, get_read_func_from_edgelist


def kernel_stream_demo(args: Dict[str, Any]):
    path = args["<edge_list_file>"]
    read_func = get_read_func_from_edgelist(path)

    # Set up graphs
    kernel_exists = True
    graph = read_func(path)
    graph_no_of_edges = graph.number_of_edges()
    edges = list(graph.edges)
    k = int(args["<k>"])
    kernel = nx.Graph()
    maximal_matching: Set[Tuple[Any, Any]] = set()

    # Set up matplotlib
    mpl.rcParams["toolbar"] = "None"
    plot.show()
    figure: Figure = plot.figure("Kernelization Algorithm", figsize=(16, 9))
    figure.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9)
    figure.suptitle("Kernelization Algorithm")
    layout = get_graph_layout(graph)
    delay = float(args["--delay"]) / 1000
    with_labels = args["--label"]

    ## Graph subplot
    graph_axes: Axes = figure.add_subplot(1, 2, 1)

    ## Kernel subplot
    kernel_axes: Axes = figure.add_subplot(1, 2, 2)

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
            maximal_matching.add((u, v))
            kernel.add_edge(u, v)

            if len(maximal_matching) > k:
                figure.text(
                    0.5,
                    0.05,
                    f"There is no such kernel of size {k}",
                    fontsize=24,
                    color="white",
                    bbox={"boxstyle": "round", "facecolor": "red", "edgecolor": "red",},
                    horizontalalignment="center",
                    verticalalignment="center",
                    transform=figure.transFigure,
                )
                kernel_exists = False
                break

        # Graph subplot
        draw_graph(graph_axes, graph, kernel, layout, u, v, with_labels)

        # Kernel subplot
        draw_kernel(kernel_axes, kernel, graph, layout, maximal_matching, with_labels)

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
            color="white",
            bbox={"boxstyle": "round", "facecolor": "green", "edgecolor": "green",},
            horizontalalignment="center",
            verticalalignment="center",
            transform=figure.transFigure,
        )

    plot.show()


if __name__ == "__main__":
    args = docopt(__doc__)
    kernel_stream_demo(args)
