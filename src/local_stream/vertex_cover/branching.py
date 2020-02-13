class Branching:
    def __init__(self, no_of_edges):
        self.vertex_cover = set()
        self.bin_string_pos = 1
        self.edge_pos = 1
        self.no_of_edges = no_of_edges

    def next_edge(self, edge):
