"""Usage: branching_stream_demo.py <edge_list_file> <k> [--delay=DELAY --shuffle --layout=LAYOUT]

Demonstration of the branching algorithm applied to a graph edgelist

Arguments:
    edge_list_file      Path to a graph in the form of an edge list
    k                   Size up to which to generate a branching for

Options:
    -h --help           Show this screen
    --delay=DELAY       Specify delay between iterations in milliseconds [default: 500]
    --shuffle           Shuffles order of edges added to branching
    --layout=LAYOUT     Specify Graphviz layout [default: dot]
"""
from random import shuffle
from tkinter import TclError
from typing import Any, Dict, Iterator, Optional, Set, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plot
from docopt import docopt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.legend_handler import HandlerLine2D
from matplotlib.lines import Line2D
from matplotlib.text import Text
from networkx import Graph, balanced_tree, draw
from networkx.drawing.nx_pydot import graphviz_layout

from visuals_utils import _in, get_graph_layout, get_read_func_from_edgelist


def branching_stream_demo(args: Dict[str, Any]):
    """
    Creates a live demonstration of the branching algorithm

    Parameters
    ----------
        args : Dict[str, Any]
            Command line arguments
    """
    path = args["<edge_list_file>"]
    read_func = get_read_func_from_edgelist(path)

    # Set up graphs
    graph: Graph = read_func(path)
    edges = list(graph.edges)
    if args["--shuffle"]:
        shuffle(edges)

    k = int(args["<k>"])
    if k >= 10:
        print("k values 10 or more will take significantly longer to load")

    # Set up matplotlib
    plot.show()
    figure: Figure = plot.figure("Branching Algorithm", figsize=(16, 9))

    # Fix window to x=50 y=50 from top right of screen
    figure.canvas.manager.window.wm_geometry("+50+50")
    figure.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9)
    figure.suptitle("Branching Algorithm", fontsize=24)
    text_bin_string = figure.text(0.05, 0.85, "", fontsize=24, family="monospace")
    text_bing_string_pos = figure.text(
        0.05, 0.854, "", fontsize=24, family="monospace", weight="bold"
    )
    text_current_edge = figure.text(0.05, 0.80, "", fontsize=24, family="monospace")
    tree_axes = figure.subplots()

    tree = balanced_tree(2, k)
    layout = graphviz_layout(tree, prog=args["--layout"])
    delay = float(args["--delay"]) / 1000

    try:
        vertex_cover = _calculate_vertex_cover_and_draw(
            figure,
            edges,
            k,
            graph,
            tree,
            layout,
            tree_axes,
            delay,
            text_bin_string,
            text_bing_string_pos,
            text_current_edge,
        )
    except TclError:
        # Exception caused when exiting
        return False

    if vertex_cover is not None:
        _draw_success_text(figure, f"A Vertex Cover exists of size {len(vertex_cover)}")
    else:
        _draw_failure_text(figure, f"There is no Vertex Cover of max size {k}")

    plot.show()


def _calculate_vertex_cover_and_draw(
    figure,
    edges,
    k,
    graph,
    tree,
    layout,
    tree_axes,
    delay,
    text_bin_string,
    text_bin_string_pos,
    text_current_edge,
) -> Optional[set]:
    for bin_string in _get_binary_strings(k):
        vertex_cover: set = set()
        bin_string_pos = 0
        edge_pos = 0

        current_node = 0

        _draw(
            figure,
            tree,
            layout,
            tree_axes,
            bin_string,
            bin_string_pos,
            current_node,
            edge_pos,
            ("", ""),
            text_bin_string,
            text_bin_string_pos,
            text_current_edge,
            delay,
        )

        while bin_string_pos != k:
            u, v = edges[edge_pos]

            _draw(
                figure,
                tree,
                layout,
                tree_axes,
                bin_string,
                bin_string_pos,
                current_node,
                edge_pos,
                (u, v),
                text_bin_string,
                text_bin_string_pos,
                text_current_edge,
                delay,
            )

            if u not in vertex_cover and v not in vertex_cover:
                edge_sm, edge_bg = (u, v) if u < v else (v, u)

                if bin_string[bin_string_pos] == "0":
                    vertex_cover.add(edge_sm)
                else:
                    vertex_cover.add(edge_bg)

                bin_string_pos += 1
            edge_pos += 1

            current_node = _get_node_index(bin_string, bin_string_pos - 1)
            _draw(
                figure,
                tree,
                layout,
                tree_axes,
                bin_string,
                bin_string_pos,
                current_node,
                edge_pos,
                (u, v),
                text_bin_string,
                text_bin_string_pos,
                text_current_edge,
                delay,
            )

            if edge_pos == graph.number_of_edges():
                return vertex_cover

    return None


def _get_binary_strings(k) -> Iterator[str]:
    """
    Generates binary strings up to a given length k

    Yields
    ------
        str
            Incrementing binary strings
    """
    for i in range(2 ** k):
        yield bin(i)[2:].rjust(k, "0")


def _draw(
    figure: Figure,
    tree: Graph,
    layout: dict,
    tree_axes: Axes,
    bin_string: str,
    bin_string_pos: int,
    current_node: int,
    edge_pos: int,
    current_edge,
    text_bin_string,
    text_bin_string_pos,
    text_current_edge,
    delay,
):
    tree_axes.clear()
    tree_axes.set_title(
        f"i={bin_string_pos}, j={edge_pos}", fontsize=20,
    )

    # highlight current node
    node_colours = [
        "yellow" if i == current_node else "#1f78b4"
        for i in range(tree.number_of_nodes())
    ]

    # bolden path
    path = []
    if current_node > 0:
        path.append((0, _get_node_index(bin_string, 0)))
        for i in range(bin_string_pos - 1):
            if i + 1 > bin_string_pos:
                break

            u_index = _get_node_index(bin_string, i)
            v_index = _get_node_index(bin_string, i + 1)
            path.append((u_index, v_index))

    edge_widths = [3 if edge in path else 1 for edge in tree.edges]

    draw(tree, pos=layout, ax=tree_axes, node_color=node_colours, width=edge_widths)

    text_bin_string.set_text(bin_string)
    text_bin_string_pos.set_text(" " * bin_string_pos + "_")
    text_current_edge.set_text(current_edge)

    # Wait for update
    plot.pause(delay)


def _get_node_index(bin_string, bin_string_pos):
    return 2 ** (bin_string_pos + 1) - 1 + int(bin_string[: (bin_string_pos + 1)], 2)


def _draw_success_text(figure, text):
    _draw_result_text(figure, text, "green")


def _draw_failure_text(figure, text):
    _draw_result_text(figure, text, "red")


def _draw_result_text(figure, text, colour):
    figure.text(
        0.5,
        0.05,
        text,
        fontsize=24,
        color="white",
        bbox={"boxstyle": "round", "facecolor": colour, "edgecolor": colour,},
        horizontalalignment="center",
        verticalalignment="center",
        transform=figure.transFigure,
    )


if __name__ == "__main__":
    args = docopt(__doc__)
    branching_stream_demo(args)
