from typing import Iterator, Optional, TextIO, Tuple


class Branching:
    def __init__(self, k, no_of_edges):
        self.k = k
        self.no_of_edges = no_of_edges

        self.edge_pos = 0

    def calculate_vc(self, stream: TextIO) -> Optional[set]:
        for bin_string in self._get_binary_strings():
            # Return stream to start
            stream.seek(0)
            # Ignore number of nodes and edges
            stream.readline()

            vertex_cover: set = set()
            bin_string_pos = 0
            self.edge_pos = 0

            while bin_string_pos != self.k:
                u, v = stream.readline().split()[:2]

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
