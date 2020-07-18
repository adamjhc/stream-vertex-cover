"""Usage: convert_edgelist_to_labelled_edgelist.py <input>

Arguments:
    input   Path to edge list file or dir
"""
import os
from pathlib import Path

from docopt import docopt

from tqdm import tqdm


def convert_edgelist_to_labelled_edgelist(edgelist_path: str):
    """Converts an edgelist file to a labelled edgelist

    Arguments
    ---------
        edgelist_path : str
            File path to edgelist
    """
    nodes = set()
    num_edges = 0
    with open(edgelist_path, "r") as edgelist:
        for line in tqdm(
            edgelist, total=0, leave=False, desc="Reading edge list", unit=" edges"
        ):
            u, v = line.split()[:2]
            nodes.add(u)
            nodes.add(v)
            num_edges += 1

        edgelist.seek(0)
        with open(f"{Path(edgelist_path).stem}_labelled.txt", "w") as output:
            output.write(f"{len(nodes)} {num_edges}\n")
            for line in tqdm(
                edgelist,
                total=num_edges,
                leave=False,
                desc="Writing labelled edge list",
                unit=" edges",
            ):
                output.write(line)


if __name__ == "__main__":
    args = docopt(__doc__)

    path = args["<input>"]
    if os.path.isfile(path):
        convert_edgelist_to_labelled_edgelist(path)
    elif os.path.isdir(path):
        for file in os.listdir(path):
            if file.endswith(".txt"):
                convert_edgelist_to_labelled_edgelist(f"{path}/{file}")
