"""
This is a script to export NetworkX graphs into a streamable format

Format
------

<Number of edges>
u v
u v
u v
"""
import networkx as nx
from networkx import Graph
from typing import Dict


def export_networkx_graphs():
    graphs: Dict[str, Graph] = {
        "tutte": nx.tutte_graph(),
        "petersen": nx.petersen_graph(),
        "floretine_families": nx.florentine_families_graph(),
        "karate_club": nx.karate_club_graph(),
        "les_miserables": nx.les_miserables_graph(),
    }

    for name, graph in graphs.items():
        edges = list(graph.edges)

        with open(name + ".txt", "x") as output:
            output.write(f"{len(edges)}\n")
            for u, v in edges:
                output.write(f"{u} {v}\n")


if __name__ == "__main__":
    export_networkx_graphs()
