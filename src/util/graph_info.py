import networkx as nx


class GraphInfo:
    def __init__(self, graph: nx.Graph):
        self.nodes = graph.number_of_nodes()
        self.edges = graph.number_of_edges()
        self.density = nx.density(graph)
        self.transitivity = nx.transitivity(graph)
        self.clustering_coefficient = nx.average_clustering(graph)
        self.triangles = int(sum(nx.triangles(graph).values()) / 3)
        self.fraction_closed_triangles = self.triangles / self._count_paths(graph, 2)

    def to_csv(
        self,
        dataset: str,
        desc: str,
        filename: str,
        category: str,
        source: str,
        link: str,
    ) -> str:
        return ",".join(
            [
                dataset,
                desc,
                filename,
                str(self.nodes),
                str(self.edges),
                str(round(self.density, 3)),
                str(round(self.transitivity, 3)),
                str(round(self.clustering_coefficient, 4)),
                str(self.triangles),
                str(round(self.fraction_closed_triangles, 4)),
                category,
                source,
                link,
            ]
        )

    def _count_paths(self, graph: nx.Graph, length: int):
        all_paths = []
        for node in graph:
            all_paths.extend(self._find_paths(graph, node, length))

        return len(all_paths)

    def _find_paths(self, graph: nx.Graph, u, length: int):
        if length == 0:
            return [[u]]

        return [
            [u] + path
            for neighbor in graph.neighbors(u)
            for path in self._find_paths(graph, neighbor, length - 1)
            if u not in path
        ]


if __name__ == "__main__":
    pass
