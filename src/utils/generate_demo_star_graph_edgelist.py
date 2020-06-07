"""Usage: generate_demo_star_graph_edgelist.py <number_of_stars> <number_of_neighbours>

Arguments:

"""
from typing import Any, Dict

import matplotlib.pyplot as plot
from docopt import docopt
from networkx import Graph, disjoint_union, draw, star_graph, write_edgelist


def main(args: Dict[str, Any]):
    no_of_stars = int(args["<number_of_stars>"])
    no_of_neighbours = int(args["<number_of_neighbours>"])

    graph = Graph()

    for _ in range(no_of_stars):
        star = star_graph(no_of_neighbours)
        graph = disjoint_union(graph, star)

    size_of_stars = no_of_neighbours + 1
    for i in range(0, no_of_stars * size_of_stars - size_of_stars, size_of_stars,):
        graph.add_edge(i, i + size_of_stars)

    # show graph
    plot.subplot(1, 1, 1)
    draw(graph)
    plot.show()

    # export
    confirm = input("This good? [Y/n]: ")
    if confirm == "" or confirm.lower() == "y":
        write_edgelist(
            graph,
            f"connected_star_graph_{no_of_stars}_{no_of_neighbours}.txt",
            data=False,
        )


if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)
