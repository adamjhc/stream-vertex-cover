"""
Usage:
    vc_stream.py branching FILE <k> [--log=LEVEL]
    vc_stream.py kernel-exists FILE <k> [--log=LEVEL]
    vc_stream.py kernel-br FILE <k> [--log=LEVEL]
    vc_stream.py kernel-min FILE

Stream a file through a specified algorithm to calculate the vertex cover

Arguments:
    FILE            The input file to stream edges from
    k               The k value

Options:
    -h --help       Show this screen
    --log=LEVEL     Specify the log level [default: INFO]
"""
import logging
import os
from datetime import datetime
from math import ceil, log2
from typing import Any, Dict, Optional

from docopt import docopt
from tqdm import tqdm

from branching import Branching
from kernel import Kernel


def main(args: Dict[str, Any]):
    filename = args["FILE"]
    if args["kernel-min"]:
        kernel_min(filename)
    else:
        _init_logging(args["--log"])

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
    stream = open(filename)
    start = 0
    # upper bound is the number of nodes
    end = int(stream.readline().split()[0])
    stream.close()

    with tqdm(total=ceil(log2(end)), desc="Binary Search for min-k") as pbar:
        min_k = end
        while start <= end:
            mid = (start + end) // 2
            if _kernelize(filename, mid, False) is not None:
                min_k = mid
                end = mid - 1
            else:
                start = mid + 1

            pbar.update(1)

    print(min_k)


def kernel_br(filename: str, k: int):
    """Finds a vertex cover if one exists of at most size k

    First kernelises the graph and then runs it through the branching method

    Arguments
    ---------
        filename : str
            The file path to stream from
        k : int
            Maximum size of vertex cover
    """
    kernel = _kernelize(filename, k)
    if not kernel:
        return None

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
    print(_kernelize(filename, k) is not None)


def branching(filename: str, k: int):
    """Finds a vertex cover if one exists of at most size k

    Uses the branching method

    Arguments
    ---------
        filename : str
            The file path to stream from
        k : int
            Maximum size of vertex cover

    Returns
    -------
        set
            Vertex cover if one exists else None
    """
    with open(filename) as stream:
        # First line of stream will give us the number of nodes and edges
        no_of_edges = int(stream.readline().split()[1])

        branching = Branching(k, no_of_edges)

        print(branching.calculate_vc(stream))


def _kernelize(filename: str, k: int, leave_pbar: bool = True) -> Optional[Kernel]:
    with open(filename) as stream:
        edges = int(stream.readline().split()[1])

        kernel = Kernel(k)

        with tqdm(total=edges, leave=leave_pbar, desc="Edges") as pbar:
            for line in stream:
                u, v = line.split()[:2]

                if not kernel.next(u, v):
                    return None

                pbar.update(1)

        return kernel


def _init_logging(log_level):
    logging.basicConfig(
        level=logging._checkLevel(log_level),
        filename="log.csv",
        # filename=datetime.now().strftime("vc_stream_%Y-%m-%d_%H-%M-%S.csv"),
        format="%(asctime)s,%(levelname)s,%(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
    )


if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)
