import networkx as nx

from networkx import Graph


def read_dimacs(path: str) -> Graph:
    with open(path, "r") as file:
        graph = nx.Graph()

        for line in file.readline():
            line_type = line[0]

            if line_type == "e" or line_type == "a":
                attributes = line.split()
                u = int(attributes[1])
                v = int(attributes[2])

                w: int
                if len(attributes) > 3:
                    w = int(attributes[3])

                graph.add_edge(u, v, weight=w)
            elif line_type == "c":
                continue
            elif line_type == "p":
                continue

    return graph


def read_labelled_edgelist(path: str) -> Graph:
    with open(path, "r") as file:
        # ignore first line
        file.readline()

        return nx.parse_edgelist(file)
