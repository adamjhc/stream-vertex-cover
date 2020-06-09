"""Usage: kernel_stream_animation.py <edge_list_file> <k> <output_name> [options]

Creates an animation of the kernelization of a graph edgelist

Arguments:
    edge_list_file          Path to a graph in the form of an edge list
    k                       Size up to which to generate a kernel for
    output_name             Name and extension of the output file

Options:
    -h --help               Show this screen
    --interval=INTERVAL     Delay between frames in milliseconds [default: 200]
    --repeat-delay=DELAY    Delay before repeating in milliseconds [default: 500]
    --width=WIDTH           Width of GIF in pixels [default: 800]
    --height=HEIGHT         Height of GIF in pixels [default: 450]
    --label                 Show labels on nodes
    --shuffle               Shuffle order of edges added to kernel
"""
from random import shuffle
from typing import Any, Dict, Set, Tuple

import matplotlib.pyplot as plot
import networkx as nx
from docopt import docopt
from matplotlib import animation
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.legend_handler import HandlerLine2D
from matplotlib.lines import Line2D
from networkx import Graph
from tqdm import tqdm

from kernel_utils import draw_failure_text, draw_graph, draw_kernel, draw_success_text
from visuals_utils import _in, get_graph_layout, get_read_func_from_edgelist


def kernel_stream_animation(args: Dict[str, Any]):
    path = args["<edge_list_file>"]
    read_func = get_read_func_from_edgelist(path)

    # Set up graphs
    kernel_exists = True
    graph = read_func(path)

    edges = list(graph.edges)
    if args["--shuffle"]:
        shuffle(edges)

    k = int(args["<k>"])
    kernel = nx.Graph()
    maximal_matching: Set[Tuple[Any, Any]] = set()

    # Build plot
    pixel_density = 100
    figure, (graph_axes, kernel_axes) = plot.subplots(
        1,
        2,
        figsize=(
            float(args["--width"]) / pixel_density,
            float(args["--height"]) / pixel_density,
        ),
        dpi=pixel_density,
    )
    figure.suptitle("Kernelization Algorithm")
    layout = get_graph_layout(graph)

    anim = animation.FuncAnimation(
        figure,
        update,
        frames=len(edges),
        interval=int(args["--interval"]),
        fargs=(
            figure,
            graph_axes,
            kernel_axes,
            layout,
            graph,
            kernel,
            maximal_matching,
            k,
            kernel_exists,
            edges,
            args["--label"],
        ),
        repeat_delay=int(args["--repeat-delay"]),
    )

    progress_bar = tqdm(
        total=len(edges), leave=False, desc="Drawing frames", unit=" frames", initial=1,
    )
    anim.save(
        args["<output_name>"],
        writer="imagemagick",
        progress_callback=lambda i, n: progress_bar.update(1)
        if i < n - 1
        else progress_bar.set_description("Rendering"),
    )
    progress_bar.close()


def update(
    i: int,
    figure: Figure,
    graph_axes: Axes,
    kernel_axes: Axes,
    layout: dict,
    graph: Graph,
    kernel: Graph,
    maximal_matching: Set[Tuple[Any, Any]],
    k: int,
    kernel_exists,
    edges: list,
    with_labels: bool,
):
    u, v = edges[i]

    # Kernelization algorithm
    if kernel_exists:
        is_neighbour = False
        if _in(u, maximal_matching):
            is_neighbour = True
            if kernel.degree[u] < k:
                kernel.add_edge(u, v)

        if _in(v, maximal_matching):
            is_neighbour = True
            if kernel.degree[v] < k:
                kernel.add_edge(u, v)

        if not is_neighbour:
            maximal_matching.add((u, v))
            kernel.add_edge(u, v)

            if len(maximal_matching) > k:
                kernel_exists = False

    if not kernel_exists:
        draw_failure_text(figure, f"There is no such kernel of size {k}")
    elif i == len(edges) - 1:
        draw_success_text(figure, f"A kernel exists of size {k}")

    ## Graph subplot
    draw_graph(graph_axes, graph, kernel, layout, u, v, with_labels)

    ## Kernel subplot
    draw_kernel(kernel_axes, kernel, graph, layout, k, maximal_matching, with_labels)


if __name__ == "__main__":
    args = docopt(__doc__)
    kernel_stream_animation(args)
