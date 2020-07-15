"""
Usage:
    local_stream.py branching FILE <k>
    local_stream.py kernel-exists FILE <k>
    local_stream.py kernel-br FILE <k>
    local_stream.py kernel-min FILE

Stream a labelled edge list through a specified algorithm to calculate
information relating to vertex cover.

Arguments:
    branching       Use a branching method to calculate a vertex cover
    kernel-exists   See if a kernel exists for a given size k
    kernel-br       Kernelize a given file and then run branching to get a vc
    kernel-min      Use binary search to find the minimum kernel size
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
from tqdm import tqdm

from local_stream_branching import Branching
from local_stream_kernel import Kernel


def main(args: Dict[str, Any]):
    filename = args["FILE"]
    if args["kernel-min"]:
        kernel_min(filename)
    else:
        k = int(args["<k>"])
        if args["branching"]:
            branching(filename, k)
        elif args["kernel-exists"]:
            kernel_exists(filename, k)
        elif args["kernel-br"]:
            kernel_br(filename, k)


def kernel_min(filename: str):
    """Finds the minimum size of a kernel for a given stream of edges

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

    kernel: Optional[Kernel]
    min_k = end
    with tqdm(
        total=ceil(log2(end)), desc="Binary Search for min-k", leave=False
    ) as pbar:
        while start <= end:
            mid = (start + end) // 2
            kernel = _kernelize(filename, mid)
            if kernel is not None:
                min_k = mid
                end = mid - 1
            else:
                start = mid + 1

            pbar.update(1)

    if kernel is not None:
        kernel_nodes = kernel.number_of_nodes()
        kernel_edges = kernel.number_of_edges()

        result_table = SingleTable(
            [
                ("Graph Name", Path(filename).stem),
                ("Graph Nodes", graph_nodes),
                ("Graph Edges", graph_edges),
                ("Min k", min_k),
                ("Kernel Nodes", kernel_nodes),
                ("Kernel Edges", kernel_edges),
                (
                    "Reduction",
                    f"{round(100 - ((kernel_edges / int(graph_edges)) * 100), 2)}%",
                ),
            ],
            title="Result",
        )
        result_table.inner_heading_row_border = False
        print(result_table.table)
    else:
        print("No Kernel Exists")


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
    with open(filename) as stream:
        no_of_edges = int(stream.readline().split()[1])

        branching = Branching(k, no_of_edges)

        print(branching.calculate_vc(stream))


def _kernelize(filename: str, k: int) -> Optional[Kernel]:
    """Generates a kernel for a given filepath and k value

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
        with tqdm(total=no_of_edges, leave=False, desc="Edges") as pbar:
            for line in stream:
                u, v = line.split()[:2]

                if not kernel.next(u, v):
                    kernel_exists = False
                    break

                pbar.update(1)

        return kernel if kernel_exists else None


if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)
