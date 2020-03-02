import networkx as nx

from networkx import Graph


def read_dimacs(path: str) -> Graph:
    with open(path, "r") as file:
        graph = nx.Graph()

        problem_line_seen = False

        for line in file.readline():
            line_type = line[0]

            if line_type == "c":
                continue
            elif line_type == "p":
                problem_line_seen = True
            elif line_type == "e" or line_type == "a":
                if not problem_line_seen:
                    raise Exception(
                        "Bad DIMACS format: edge descriptor seen before problem descriptor"
                    )

                attributes = line.split()
                u = attributes[1]
                v = attributes[2]
                graph.add_edge(u, v)

    return graph
