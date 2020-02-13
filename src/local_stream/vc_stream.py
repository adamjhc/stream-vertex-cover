"""Usage: vc_stream.py (-b | -k) FILE [--log=LEVEL]

Stream a file through a specified algortihm to calculate the vertex cover

Arguments:
    FILE            The input file to stream edges from
    LEVEL           The level to log at (NONE,INFO,DEBUG)

Options:
    -h --help       Show this screen
    -b              Use the branching algorithm
    -k              Use the kernel algorithm
    --log=LEVEL     Specify the log level [default: INFO]
"""
from docopt import docopt
import logging
from datetime import datetime


def main(arguments: dict):
    init_logging(arguments["--log"])

    if arguments["-b"]:
        branching(arguments["FILE"])
    else:
        kernel(arguments["FILE"])


def branching(filename: str):
    pass
    # with open(filename) as stream:
    #     # First line of stream will give us the number of edges
    #     no_of_edges = int(stream.readline())

    #     # Every following line is an edge
    #     for line in stream:
    #         edge = line.split()


def kernel(filename: str):
    pass


def init_logging(log_level):
    logging.basicConfig(
        level=logging._checkLevel(log_level),
        filename="log.csv",
        # filename=datetime.now().strftime("vc_stream_%Y-%m-%d_%H-%M-%S.csv"),
        format="%(asctime)s,%(levelname)s,%(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
    )


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main(arguments)
