"""
Usage: 
    vc_stream.py branching FILE <k> [--log=LEVEL]
    vc_stream.py kernel FILE <k> [--log=LEVEL]
    vc_stream.py kernel-br FILE <k> [--log=LEVEL]
    vc_stream.py kernel-min FILE

Stream a file through a specified algorithm to calculate the vertex cover

Arguments:
    FILE            The input file to stream edges from
    k               The k value

Options:
    -h --help       Show this screen
    -b              Use the branching algorithm
    -k              Use the kernel algorithm
    --log=LEVEL     Specify the log level [default: INFO]
"""
import logging
from datetime import datetime
from typing import Any, Dict

from docopt import docopt

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
        elif args["kernel"]:
            kernel(filename, k)
        elif args["kernel-br"]:
            kernel_br(filename, k)


def kernel_min(filename: str):
    stream = open(filename)
    start = 0
    # upper bound is the number of nodes
    end = int(stream.readline().split()[0])
    stream.close()

    min_k = end
    while start <= end:
        mid = (start + end) // 2
        if _kernelize(filename, mid) is not None:
            min_k = mid
            end = mid - 1
        else:
            start = mid + 1

    print(min_k)


def kernel_br(filename: str, k: int):
    pass


def kernel(filename: str, k: int):
    print(_kernelize(filename, k) is not None)


def branching(filename: str, k: int):
    pass
    # with open(filename) as stream:
    #     # First line of stream will give us the number of edges
    #     no_of_edges = int(stream.readline())

    #     # Every following line is an edge
    #     for line in stream:
    #         edge = line.split()


def _kernelize(filename: str, k: int) -> Kernel:
    with open(filename) as stream:
        # First line of stream will give us the number of nodes and edges which
        # we don't need in this case
        stream.readline()

        kernel = Kernel(k)

        # Every following line is an edge
        for line in stream:
            edges = line.split()

            if not kernel.next(edges[0], edges[1]):
                return None

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
