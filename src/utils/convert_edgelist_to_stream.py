"""Usage: convert_edgelist_to_stream.py <input> <output>

Arguments:
    input   Path to edgelist file
    output  Path to output file
"""
import networkx as nx
from docopt import docopt


def convert_edgelist_to_stream(edgelist_path: str, output_path: str):
    # Check whether given edgelist is weighted
    read_func = nx.read_edgelist
    with open(edgelist_path, "r") as edgelist:
        line = edgelist.readline()
        if len(line.split()) > 2:
            read_func = nx.read_weighted_edgelist

    graph = read_func(edgelist_path)
    with open(output_path, "x") as output:
        output.write(f"{graph.number_of_nodes()} {graph.number_of_edges()}\n")
        for line in nx.generate_edgelist(graph, data=False):
            output.write(f"{line}\n")


if __name__ == "__main__":
    args = docopt(__doc__)
    convert_edgelist_to_stream(args["<input>"], args["<output>"])
