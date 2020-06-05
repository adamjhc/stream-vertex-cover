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
    --width=WIDTH           Width of GIF in pixels [default: 640]
    --height=HEIGHT         Height of GIF in pixels [default: 480]
    --label                 Show labels on nodes
"""
from typing import Any, Dict, Set, Tuple

import matplotlib.pyplot as plot
import networkx as nx
from docopt import docopt
from matplotlib import animation
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from networkx import Graph

from visuals_util import _in, get_graph_layout, get_read_func_from_edgelist


def kernel_stream_animation(args: Dict[str, Any]):
    path = args["<edge_list_file>"]
    read_func = get_read_func_from_edgelist(path)

    # Set up graphs
    graph = read_func(path)
    edges = list(graph.edges)
    k = int(args["<k>"])
    kernel = nx.Graph()
    maximal_matching: Set[Tuple[Any, Any]] = set()

    # Build plot
    pixel_density = 100
    fig, ax = plot.subplots(
        figsize=(
            float(args["--fig-width"]) / pixel_density,
            float(args["--fig-height"]) / pixel_density,
        ),
        dpi=pixel_density,
    )
    fig.suptitle("Kernelization Algorithm")
    layout = get_graph_layout(graph)

    anim = animation.FuncAnimation(
        fig,
        update,
        frames=len(edges),
        interval=int(args["--interval"]),
        fargs=(ax, layout, kernel, maximal_matching, k, edges, args["--label"]),
        repeat_delay=int(args["--repeat-delay"]),
    )
    anim.save(args["<output_name>"], writer="imagemagick")


def update(
    i: int,
    ax: Axes,
    layout: dict,
    kernel: Graph,
    maximal_matching: Set[Tuple[Any, Any]],
    k: int,
    edges: list,
    with_labels: bool,
):
    ax.clear()

    u, v = edges[i]

    # Kernelization algorithm
    if len(maximal_matching) <= k:
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

    # matplotlib updates
    title = f"Iteration {i}"
    if len(maximal_matching) > k:
        title += f" - No kernel for k = {k}"
    ax.set_title(title)

    # Red colour for nodes in the matching
    node_colours = [
        "r" if _in(node, maximal_matching) else "k" for node in kernel.nodes
    ]

    # Smaller node for nodes not in the matching
    node_sizes = [
        100 if not _in(node, maximal_matching) else 300 for node in kernel.nodes
    ]

    # Red colour for edges between two matched nodes
    edge_colours = ["r" if (u, v) in maximal_matching else "k" for u, v in kernel.edges]

    # Thicker edge for edges between edges in matching
    edge_widths = [2 if edge in maximal_matching else 0.5 for edge in kernel.edges]

    nx.draw(
        kernel,
        pos=layout,
        with_labels=with_labels,
        node_color=node_colours,
        node_size=node_sizes,
        edge_color=edge_colours,
        width=edge_widths,
    )


if __name__ == "__main__":
    args = docopt(__doc__)
    kernel_stream_animation(args)
