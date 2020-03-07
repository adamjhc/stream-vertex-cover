"""Usage: convert_edgelist_to_labelled_edgelist.py <input> <output>

Arguments:
    input   Path to edgelist file
    output  Path to output file
"""
from docopt import docopt
from tqdm import tqdm


def convert_edgelist_to_labelled_edgelist(edgelist_path: str, output_path: str):
    """Converts an edgelist file to a labelled edgelist

    Arguments
    ---------
        edgelist_path : str
            File path to edgelist
        output_path : str
            File path to output
    """
    nodes = set()
    edges = 0
    with open(edgelist_path, "r") as edgelist:
        for line in tqdm(
            edgelist, total=0, leave=False, desc="Reading edge list", unit=" edges"
        ):
            u, v = line.split()[:2]
            nodes.add(u)
            nodes.add(v)
            edges += 1

        edgelist.seek(0)
        with open(output_path, "x") as output:
            output.write(f"{len(nodes)} {edges}\n")
            for line in tqdm(
                edgelist,
                total=edges,
                leave=False,
                desc="Writing labelled edge list",
                unit=" edges",
            ):
                output.write(line)


if __name__ == "__main__":
    args = docopt(__doc__)
    convert_edgelist_to_labelled_edgelist(args["<input>"], args["<output>"])
