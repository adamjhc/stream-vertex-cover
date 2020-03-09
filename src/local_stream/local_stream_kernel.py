from typing import Any, Optional


class Kernel:
    def __init__(self, k: int):
        """
        """
        self.k = k
        self.matching: dict = {}

    def next(self, u: Any, v: Any) -> bool:
        """
        """
        is_neighbour = False

        match = self._get_if_in(u, self.matching)
        if match is not None and len(match.neighbours_u) <= self.k:
            match.neighbours_u.append((u, v))
            is_neighbour = True

        match = self._get_if_in(v, self.matching)
        if match is not None and len(match.neighbours_v) <= self.k:
            match.neighbours_v.append((u, v))
            is_neighbour = True

        if not is_neighbour:
            self.matching[(u, v)] = Match()

            if len(self.matching) > self.k:
                return False

        return True

    def export(self, path: str):
        """
        """
        pass

    def _get_if_in(self, item, dictn: dict) -> Optional[Any]:
        """
        """
        for pair, match in dictn.items():
            if item in pair:
                return match

        return None


class Match:
    def __init__(self):
        """
        """
        self.neighbours_u = []
        self.neighbours_v = []
