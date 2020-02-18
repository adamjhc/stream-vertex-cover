import networkx as nx


class GraphInfo:
    def __init__(self, graph: nx.Graph):
        self.nodes = graph.number_of_nodes()
        self.edges = graph.number_of_edges()
        self.density = nx.density(graph)
        self.transitivity = nx.transitivity(graph)
        self.clustering_coefficient = nx.average_clustering(graph)
        self.triangles = nx.triangles(graph)
        self.fraction_closed_triangles = 0

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
                str(len(self.triangles)),
                str(round(self.fraction_closed_triangles, 4)),
                category,
                source,
                link,
            ]
        )


if __name__ == "__main__":
    pass
