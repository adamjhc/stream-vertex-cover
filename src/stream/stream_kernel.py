from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from faust import ChannelT, StreamT
from terminaltables import SingleTable

from stream_models import JobInfo


async def handle_kernel(
    stream_edges: StreamT,
    channel_edges: ChannelT,
    channel_results: ChannelT,
    job_no: str,
    job: JobInfo,
):
    kernel = Kernel(job.k)
    kernel_exists = True

    async for i, edge in stream_edges.enumerate(start=0):
        if edge.is_end:
            break

        if not kernel_exists:
            continue

        await channel_edges.put(edge)

        if not kernel.next(edge.u, edge.v):
            kernel_exists = False

    graph_edges = i
    kernel_edges = kernel.number_of_edges()

    result = [
        ("Algorithm", job.algorithm),
        ("Graph Name", Path(job.path).stem),
        ("Graph Edges", graph_edges),
        ("k", job.k),
        ("Kernel exists?", kernel_exists),
    ]

    if kernel_exists:
        result.extend(
            [
                ("Kernel Edges", kernel_edges),
                (
                    "Reduction",
                    f"{100 - round(100 - ((kernel_edges / graph_edges) * 100), 2)}%",
                ),
            ]
        )

    result_table = SingleTable(result, title=f"Job {job_no}")
    result_table.inner_heading_row_border = False

    for line in result_table.table.splitlines():
        await channel_results.put(line)


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

    def number_of_edges(self):
        """
        """
        no_of_edges = 0
        for neighbours in self.matching.values():
            no_of_edges += 1 + len(neighbours[0]) + len(neighbours[1])

        return no_of_edges

    def _get_if_in(
        self, item, dictn: dict
    ) -> Optional[Tuple[Tuple[Any, Any], Tuple[List[Any], List[Any]]]]:
        """
        """
        for pair, match in dictn.items():
            if item in pair:
                return pair, match

        return None


if __name__ == "__main__":
    pass
