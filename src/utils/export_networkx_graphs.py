"""
This is a script to export NetworkX graphs into a labelled edge list

Format
------

<Number of nodes> <Number of edges>
u v
u v
u v
"""
import networkx as nx
from networkx import Graph


def export_networkx_graphs():
    graphs = {
        "tutte": nx.tutte_graph(),
        "petersen": nx.petersen_graph(),
        "floretine_families": nx.florentine_families_graph(),
        "karate_club": nx.karate_club_graph(),
        "les_miserables": nx.les_miserables_graph(),
    }

    for name, graph in graphs.items():
        with open(name + ".txt", "x") as output:
            output.write(f"{graph.number_of_nodes()} {graph.number_of_edges()}\n")
            for line in nx.generate_edgelist(graph, data=False):
                output.write(f"{line}\n")


if __name__ == "__main__":
    export_networkx_graphs()
