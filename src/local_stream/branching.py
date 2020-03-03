from io import TextIOWrapper
from typing import Iterator, Optional, Tuple


class Branching:
    def __init__(self, k, no_of_edges):
        self.k = k
        self.no_of_edges = no_of_edges

        self.edge_pos_prev = -1
        self.edge_pos = 0
        self.edge_current = None

    def calculate_vc(self, stream: TextIOWrapper) -> Optional[set]:
        for bin_string in self._get_binary_strings():
            # Return stream to start
            stream.seek(0)
            # Ignore number of nodes and edges
            stream.readline()

            vertex_cover: set = set()
            bin_string_pos = 0
            self.edge_pos = 0
            self.edge_pos_prev = -1

            while bin_string_pos != self.k:
                u, v = self._get_edge(stream)

                if u not in vertex_cover and v not in vertex_cover:
                    edge_sm, edge_bg = (u, v) if u < v else (v, u)

                    if bin_string[bin_string_pos] == "0":
                        vertex_cover.add(edge_sm)
                    else:
                        vertex_cover.add(edge_bg)

                    bin_string_pos += 1
                self.edge_pos += 1

            if self.edge_pos == self.no_of_edges:
                return vertex_cover

        return None

    def _get_binary_strings(self) -> Iterator[str]:
        """
        Generates binary strings up to a given length k

        Yields
        ------
            str
                Incrementing binary strings
        """
        for i in range(2 ** self.k):
            yield bin(i)[2:].rjust(self.k, "0")

    def _get_edge(self, stream: TextIOWrapper) -> Tuple:
        """

        """
        if self.edge_pos != self.edge_pos_prev:
            self.edge_current = stream.readline().split()[:2]
            self.edge_pos_prev = self.edge_pos

        return self.edge_current
