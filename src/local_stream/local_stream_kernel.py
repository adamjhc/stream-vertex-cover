from typing import Any, Dict, List, Optional, Tuple


class Kernel:
    def __init__(self, k: int):
        """
        """
        self.k = k
        self.matching: Dict[Tuple[Any, Any], Tuple[List[Any], List[Any]]] = {}

    def next(self, u: Any, v: Any) -> bool:
        """
        """
        is_neighbour = False

        matching = self._get_if_in(u, self.matching)
        if matching is not None:
            is_neighbour = True

            matched_edge, neighbours = matching
            vertex_pos = matched_edge.index(u)
            if len(neighbours[vertex_pos]) < self.k:
                neighbours[vertex_pos].append((u, v))

        else:
            matching = self._get_if_in(v, self.matching)
            if matching is not None:
                is_neighbour = True

                matched_edge, neighbours = matching
                vertex_pos = matched_edge.index(v)
                if len(neighbours[vertex_pos]) < self.k:
                    neighbours[vertex_pos].append((u, v))

        if not is_neighbour:
            self.matching[(u, v)] = ([], [])

            if len(self.matching) > self.k:
                return False

        return True

    def export(self, path: str):
        """
        """
        pass

    def number_of_nodes(self):
        """
        """
        nodes = set()
        for matched_edge, neighbours in self.matching.items():
            nodes.update(matched_edge)
            for edge in neighbours[0]:
                nodes.update(edge)
            for edge in neighbours[1]:
                nodes.update(edge)

        return len(nodes)

    def number_of_edges(self):
        """
        """
        no_of_edges = 0
        for neighbours in self.matching.values():
            no_of_edges += 1 + len(neighbours[0]) + len(neighbours[1])

        return no_of_edges

    def size_of_matching(self):
        """
        """
        return len(self.matching)

    def _get_if_in(
        self, item, dictn: dict
    ) -> Optional[Tuple[Tuple[Any, Any], Tuple[List[Any], List[Any]]]]:
        """
        """
        for pair, match in dictn.items():
            if item in pair:
                return pair, match

        return None
