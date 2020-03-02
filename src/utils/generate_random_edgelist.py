"""Usage: generate_random_edgelist.py <n> <p> [(<n_end> <p_end> [--n_step=NSTEP --p_step=PSTEP])]

Arguments:
    n               Number of nodes
    p               Probability for edge creation
    n_end           Upper bound (inclusive) of a range of n
    p_end           Upper bound (inclusive) of a range of p


Options:
    --n_step=NSTEP  Spacing between n values [default: 1]
    --p_step=PSTEP  Spacing between p values [default: 0.05]

Options:
    -h --help   Show this screen
"""
from typing import Any, Dict

import networkx as nx
import numpy as np
from docopt import docopt

from graph_info import GraphInfo


def main(args: Dict[str, Any]):
    n = int(args["<n>"])
    n_end = n
    n_step = int(args["--n_step"])
    p = float(args["<p>"])
    p_end = p
    p_step = float(args["--p_step"])

    if args["<n_end>"] is not None:
        n_end = int(args["<n_end>"])
        p_end = float(args["<p_end>"])

    n_end += n_step
    p_end += p_step
    for n in range(n, n_end, n_step):
        for p in np.arange(p, p_end, p_step):
            generate_random_edgelist(n, p)


def generate_random_edgelist(n: int, p: float):
    # Hard-code seed so that the same random graph may be generated with the
    # same n and p
    random_graph = nx.erdos_renyi_graph(n, p, seed=42)

    # Print out csv
    graph_info = GraphInfo(random_graph)
    dataset = "Erdős-Rényi"
    desc = f"G({n}-{round(p, 2)}) Erdős-Rényi graph"
    filename = f"erdos_renyi_{n}_{round(p, 2)}_edgelist.txt"
    category = "Synthetic"
    source = "NetworkX"
    link = "https://networkx.github.io/documentation/stable/reference/generated/networkx.generators.random_graphs.gnp_random_graph.html"
    print(graph_info.to_csv(dataset, desc, filename, category, source, link))

    nx.write_edgelist(random_graph, filename, data=False)


if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)
