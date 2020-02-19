from typing import Dict


class Kernel:
    def __init__(self, k: int):
        """
        """
        self.k = k
        self.matching = {}

    def next(self, u, v):
        """
        """
        is_neighbour = False
        if (match := self._get_if_in(u, self.matching)) is not None and len(
            match.neighbours_u
        ) <= self.k:
            match.neighbours_u.append((u, v))
            is_neighbour = True

        if (match := self._get_if_in(v, self.matching)) is not None and len(
            match.neighbours_v
        ) <= self.k:
            match.neighbours_v.append((u, v))
            is_neighbour = True

        if not is_neighbour:
            self.matching[(u, v)] = Match()

            if len(self.matching) > self.k:
                return False

        return True

    def export(self, path):
        """
        """
        pass

    def _get_if_in(self, item, dictn: dict):
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
