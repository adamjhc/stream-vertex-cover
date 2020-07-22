"""Usage: kernel_stream_demo.py <edge_list_file> <k> [--delay=DELAY --label --shuffle]

Demonstration of the kernelization of a graph edgelist

Arguments:
    edge_list_file      Path to a graph in the form of an edge list
    k                   Size up to which to generate a kernel for

Options:
    -h --help           Show this screen
    --delay=DELAY       Specify delay between iterations in milliseconds [default: 500]
    --label             Show labels on nodes
    --shuffle           Shuffles order of edges added to kernel
"""
from random import shuffle
from tkinter import TclError
from typing import Any, Dict, Set, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plot
from docopt import docopt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.legend_handler import HandlerLine2D
from matplotlib.lines import Line2D
from networkx import Graph

from kernel_utils import draw_failure_text, draw_graph, draw_kernel, draw_success_text
from visuals_utils import _in, get_graph_layout, get_read_func_from_edgelist


def kernel_stream_demo(args: Dict[str, Any]):
    """
    Creates a live demonstration of the kernelization algorithm

    Parameters
    ----------
        args : Dict[str, Any]
            Command line arguments
    """
    path = args["<edge_list_file>"]
    read_func = get_read_func_from_edgelist(path)

    # Set up graphs
    kernel_exists = True
    graph = read_func(path)

    edges = list(graph.edges)
    if args["--shuffle"]:
        shuffle(edges)

    k = int(args["<k>"])
    kernel: Graph = Graph()
    maximal_matching: Set[Tuple[Any, Any]] = set()

    # Set up matplotlib

    plot.show()
    figure: Figure = plot.figure("Kernelization Algorithm", figsize=(16, 9))

    # Fix window to x=50 y=50 from top right of screen
    figure.canvas.manager.window.wm_geometry("+50+50")
    figure.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9)
    figure.suptitle("Kernelization Algorithm")
    graph_axes: Axes = figure.add_subplot(1, 2, 1)
    kernel_axes: Axes = figure.add_subplot(1, 2, 2)

    layout = get_graph_layout(graph)
    delay = float(args["--delay"]) / 1000
    with_labels = args["--label"]

    for i, (u, v) in enumerate(edges):
        # Kernelization algorithm
        is_neighbour = False
        if _in(u, maximal_matching):
            is_neighbour = True
            if kernel.degree[u] < k:
                kernel.add_edge(u, v)

        elif _in(v, maximal_matching):
            is_neighbour = True
            if kernel.degree[v] < k:
                kernel.add_edge(u, v)

        if not is_neighbour:
            maximal_matching.add((u, v))
            kernel.add_edge(u, v)

            if len(maximal_matching) > k:
                kernel_exists = False
                break

        # Graph subplot
        draw_graph(graph_axes, graph, kernel, layout, u, v, with_labels)

        # Kernel subplot
        draw_kernel(
            kernel_axes, kernel, graph, layout, k, maximal_matching, with_labels, i
        )

        try:
            # Wait for update
            plot.pause(delay)
        except TclError:
            # Exception caused when exiting
            break

    if kernel_exists:
        draw_success_text(figure, f"A kernel exists of size {k}")
    else:
        draw_failure_text(figure, f"There is no such kernel of size {k}")

    plot.show()


if __name__ == "__main__":
    args = docopt(__doc__)
    kernel_stream_demo(args)
