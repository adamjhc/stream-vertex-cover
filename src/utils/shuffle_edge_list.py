"""Usage: shuffle_edge_list.py <path>

Arguments:
    path        Path to edge list

Options:
    --help -h       Show this screen
"""
from pathlib import Path
from random import shuffle

from docopt import docopt


def shuffle_edgelist(path: str):
    with open(path) as edge_list:
        edges = [edge for edge in edge_list.readlines()]
        shuffle(edges)

    with open(f"{Path(path).stem}_shuffled.txt", "w") as shuffled_file:
        shuffled_file.writelines(edges)


if __name__ == "__main__":
    args = docopt(__doc__)
    shuffle_edgelist(args["<path>"])
