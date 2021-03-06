"""
Usage:
    local_stream.py branching FILE <k>
    local_stream.py kernel-exists FILE <k>
    local_stream.py kernel-br FILE <k>
    local_stream.py branching-min FILE

Stream a labelled edge list through a specified algorithm to calculate
information relating to vertex cover.

Arguments:
    branching       Use a branching method to calculate a vertex cover
    kernel-exists   See if a kernel exists for a given size k
    kernel-br       Kernelize a given file and then run branching to get a vc
    branching-min   Use binary search to find the minimum vertex cover size
    FILE            Path to labelled edge list to stream edges from
    k               The k value

Options:
    -h --help       Show this screen
"""
import os
from datetime import datetime
from math import ceil, log2
from pathlib import Path
from typing import Any, Dict, Optional

from docopt import docopt
from terminaltables import SingleTable

from local_stream_branching import Branching
from local_stream_kernel import Kernel


def main(args: Dict[str, Any]):
    filename = args["FILE"]
    if args["branching-min"]:
        branching_min(filename)
    else:
        k = int(args["<k>"])
        if args["branching"]:
            branching(filename, k)
        elif args["kernel-exists"]:
            kernel_exists(filename, k)
        elif args["kernel-br"]:
            kernel_br(filename, k)


def branching_min(filename: str):
    """Finds the minimum size of vertex cover for a given stream of edges

    Uses a binary search

    Arguments
    ---------
        filename : str
            The file path to stream from
    """
    with open(filename) as stream:
        graph_nodes, graph_edges = stream.readline().split()[:2]

    start = 0
    # upper bound is the number of nodes
    end = int(graph_nodes)

    min_k = end
    while start <= end:
        mid = (start + end) // 2
        vertex_cover = _calculate_vertex_cover(filename, mid)
        if vertex_cover is not None:
            min_k = mid
            end = mid - 1
        else:
            start = mid + 1

    if vertex_cover is not None:
        result_table = SingleTable(
            [
                ("Graph Name", Path(filename).stem),
                ("Graph Nodes", graph_nodes),
                ("Graph Edges", graph_edges),
                ("Min Vertex Cover", min_k),
            ],
            title="Result",
        )
        result_table.inner_heading_row_border = False
        print(result_table.table)
    else:
        # Will never happen
        print("No Vertex Cover Exists")


def kernel_br(filename: str, k: int):
    """Finds a vertex cover if one exists of at most size k

    First kernelizes the graph and then runs it through the branching method

    Arguments
    ---------
        filename : str
            The file path to stream from
        k : int
            Maximum size of vertex cover
    """
    kernel = _kernelize(filename, k)
    if not kernel:
        print("No Kernel found")
        return

    kernel_file = "kernel.txt"
    kernel.export(kernel_file)

    branching(kernel_file, k)
    os.remove(kernel_file)


def kernel_exists(filename: str, k: int):
    """Finds True/False depending on whether a kernel exists for the given k

    Arguments
    ---------
        filename : str
            The file path to stream from
        k : int
            Value up to which to find whether a kernel exists
    """
    with open(filename) as stream:
        graph_nodes, graph_edges = stream.readline().split()[:2]

    kernel = _kernelize(filename, k)
    result_data = [
        ("Graph Name", Path(filename).stem),
        ("Graph Nodes", graph_nodes),
        ("Graph Edges", graph_edges),
        ("k", f"{k}"),
        ("Kernel exists", kernel is not None),
    ]

    if kernel is not None:
        kernel_edges = kernel.number_of_edges()
        kernel_nodes = kernel.number_of_nodes()

        result_data.extend(
            [
                ("Kernel Nodes", kernel_nodes),
                ("Kernel Edges", kernel_edges),
                (
                    "Reduction",
                    f"{round(100 - ((kernel_edges / int(graph_edges)) * 100), 2)}%",
                ),
            ]
        )

    result_table = SingleTable(result_data, title="Results")
    result_table.inner_heading_row_border = False
    print(result_table.table)


def branching(filename: str, k: int):
    """Finds a vertex cover if one exists of at most size k

    Uses the branching method

    Arguments
    ---------
        filename : str
            The file path to stream from
        k : int
            Maximum size of vertex cover
    """
    print(_calculate_vertex_cover(filename, k))


def _kernelize(filename: str, k: int) -> Optional[Kernel]:
    """Generates a kernel for a given file path and k value

    Arguments
    ---------
        filename : str
            The file path to stream from
        k : int
            Maximum size of vertex cover

    Returns
    -------
        Optional[Kernel]
            Kernel if one exists for the given value of k
    """
    with open(filename) as stream:
        no_of_edges = int(stream.readline().split()[1])

        kernel = Kernel(k)
        kernel_exists = True
        for line in stream:
            u, v = line.split()[:2]

            if not kernel.next(u, v):
                kernel_exists = False
                break

        return kernel if kernel_exists else None


def _calculate_vertex_cover(filename: str, k: int) -> Optional[set]:
    """Calculates Vertex Cover of max size k

    Uses branching method

    Arguments
    ---------
        filename : str
            The file path to stream from
        k : int
            Maximum size of vertex cover

    Returns
    -------
        Optional[set]
            Vertex Cover set if one exists for given value of k
    """
    with open(filename) as stream:
        no_of_edges = int(stream.readline().split()[1])

        branching = Branching(k, no_of_edges)

        return branching.calculate_vc(stream)


if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)
