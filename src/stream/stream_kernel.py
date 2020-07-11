from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from faust import ChannelT, StreamT
from terminaltables import SingleTable

from stream_models import JobInfo


async def handle_kernelization(
    stream_edges: StreamT,
    channel_edges: ChannelT,
    channel_results: ChannelT,
    job_no: str,
    job: JobInfo,
):
    """
    Handles the kernelization job type

    Parameters
    ----------
        stream_edges : StreamT
            Faust stream of edges
        channel_edges : ChannelT
            Faust channel to pass edges to
        channel_results : ChannelT
            Faust channel to pass results to
        job_no : str
            Job number
        job : JobInfo
            Information of the job
    """

    # Calculate kernel
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

    # Create results table to display on frontend
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

    # Results table is multi-line to write all lines to results channel
    for line in result_table.table.splitlines():
        await channel_results.put(line)


class Kernel:
    def __init__(self, k: int):
        """
        Initialises variables in kernelization
        """
        self.k = k
        self.maximal_matching: Dict[Tuple[Any, Any], Tuple[List[Any], List[Any]]] = {}

    def next(self, u: Any, v: Any) -> bool:
        """
        Adds next edge from stream to kernel

        Parameters
        ----------
            u : Any
                u of edge
            v : Any
                v of edge

        Returns
        -------
            bool
                True/False if kernel exists or not
        """
        is_neighbour = False

        matching = self._get_matching(u)
        if matching is not None:
            is_neighbour = True

            matched_edge, neighbours = matching
            vertex_pos = matched_edge.index(u)
            if len(neighbours[vertex_pos]) < self.k:
                neighbours[vertex_pos].append((u, v))

        else:
            matching = self._get_matching(v)
            if matching is not None:
                is_neighbour = True

                matched_edge, neighbours = matching
                vertex_pos = matched_edge.index(v)
                if len(neighbours[vertex_pos]) < self.k:
                    neighbours[vertex_pos].append((u, v))

        if not is_neighbour:
            self.maximal_matching[(u, v)] = ([], [])

            if len(self.maximal_matching) > self.k:
                return False

        return True

    def number_of_edges(self) -> int:
        """
        Counts the number of edges in the kernel

        Returns
        -------
            int
                Number of edges in kernel
        """
        no_of_edges = 0
        for neighbours in self.maximal_matching.values():
            no_of_edges += 1 + len(neighbours[0]) + len(neighbours[1])

        return no_of_edges

    def _get_matching(
        self, node: Any
    ) -> Optional[Tuple[Tuple[Any, Any], Tuple[List[Any], List[Any]]]]:
        """
        Gets matching of vertex if one exists

        Parameters
        ----------
            node : Any
                Node to find in maximal matching

        Returns
        -------
            Optional[Tuple[Tuple[Any, Any], Tuple[List[Any], List[Any]]]]
                If match exists in maximal matching then returns edge and
                neighbours else None
        """
        for edge, match in self.maximal_matching.items():
            if node in edge:
                return edge, match

        return None


if __name__ == "__main__":
    pass
