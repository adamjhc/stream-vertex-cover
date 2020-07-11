from typing import Any

from matplotlib.axes import Axes
from matplotlib.legend_handler import HandlerLine2D
from matplotlib.lines import Line2D
from networkx import Graph, draw

from visuals_utils import _in, both_in


def draw_graph(
    graph_axes: Axes,
    graph: Graph,
    kernel: Graph,
    layout: dict,
    u: Any,
    v: Any,
    with_labels: bool,
):
    """
    Draw whole graph

    Highlights current edge as well as colouring which edges are kept in the
    kernel

    Parameters
    ----------
        graph_axes : Axes
            Axes whole graph is drawn to
        graph : Graph
            Whole graph
        kernel : Graph
            Kernel
        layout : dict
            Layout of nodes
        u : Any
            u of edge
        v : Any
            v of edge
        with_labels : bool
            Whether to show labels on nodes
    """
    graph_node_type_names = ["Current", "In Kernel", "Not in Kernel"]
    graph_node_type_colours = ["y", "m", "k"]

    graph_axes.clear()
    graph_axes.set_title(
        f"Graph\nNodes: {graph.number_of_nodes()}, Edges: {graph.number_of_edges()}"
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

    draw(
        graph,
        ax=graph_axes,
        pos=layout,
        with_labels=with_labels,
        node_color=graph_node_colours,
        node_size=50,
        edge_color=graph_edge_colours,
    )


def draw_kernel(
    kernel_axes: Axes,
    kernel: Graph,
    graph: Graph,
    layout,
    k,
    maximal_matching,
    with_labels,
    i,
):
    """
    Draw kernel

    Shows matched edges in red

    Parameters
    ----------
        kernel_axes : Axes
            Axes kernel is drawn to
        kernel : Graph
            Kernel
        graph : Graph
            Whole graph
        layout : dict
            Layout of nodes
        k : int
            Value of k
        maximal_matching : Set[Tuple[Any, Any]]
            Maximal matching of kernel
        with_labels : bool
            Whether to show labels on nodes
        i : int
            Frame counter
    """
    kernel_node_type_names = ["Matched", "Neighbour"]
    kernel_node_type_colours = ["r", "k"]
    kernel_node_type_sizes = [200, 50]
    kernel_edge_type_widths = [2, 0.5]

    kernel_edges_num = kernel.number_of_edges()
    kernel_nodes_num = kernel.number_of_nodes()
    graph_edges_num = graph.number_of_edges()

    kernel_axes.clear()
    kernel_axes.set_title(
        f"Kernel (k={k}, i={i}/{graph_edges_num - 1})\nNodes: {kernel_nodes_num}, Edges: {kernel_edges_num}, Size of Graph: {kernel_edges_num/graph_edges_num * 100:.2f}%"
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
        edge_type = 0 if both_in(edge, maximal_matching) else 1

        kernel_edge_colours.append(kernel_node_type_colours[edge_type])
        kernel_edge_widths.append(kernel_edge_type_widths[edge_type])

    draw(
        kernel,
        ax=kernel_axes,
        pos=layout,
        with_labels=with_labels,
        node_color=kernel_node_colours,
        node_size=kernel_node_sizes,
        edge_color=kernel_edge_colours,
        width=kernel_edge_widths,
    )


def draw_success_text(figure, text):
    draw_text(figure, text, "green")


def draw_failure_text(figure, text):
    draw_text(figure, text, "red")


def draw_text(figure, text, colour):
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
