import logging
import os
import signal
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import faust
from faust import StreamT
from terminaltables import SingleTable

from stream_models import Edge, GraphInfo

web_port = 6066

app = faust.App("kernelizer", broker="kafka://localhost:9092", web_port=web_port)

topic_edges = app.topic("edges", key_type=str, value_type=Edge)
topic_info = app.topic("info", key_type=str, value_type=GraphInfo)


@app.task()
async def on_started():
    """
    """
    logging.info(f"Visit http://localhost:{web_port}")


@app.agent(topic_edges)
async def process_edges(edges: StreamT[Edge]):
    """
    """
    graphs = app.stream(topic_info)

    async for graph in graphs:
        kernel = Kernel(graph.k)
        kernel_exists = True

        async for i, edge in edges.enumerate(start=0):
            if edge.is_end:
                break

            if kernel_exists == False:
                continue

            if not kernel.next(edge.u, edge.v):
                kernel_exists = False

        graph_edges = i
        kernel_edges = kernel.number_of_edges()
        kernel_nodes = kernel.number_of_nodes()

        result_table = SingleTable(
            [
                ("Graph Name", Path(graph.path).stem),
                ("Graph Edges", graph_edges),
                ("k", graph.k),
                ("Kernel exists?", kernel_exists),
                ("Kernel Nodes", kernel_nodes),
                ("Kernel Edges", kernel_edges),
                (
                    "Reduction",
                    f"{round(100 - ((kernel_edges / graph_edges) * 100), 2)}%",
                ),
            ],
            title="Result",
        )
        logging.info(f"Completed kernelization\n{result_table.table}")


@app.page("/")
async def get_index(self, request):
    """
    """
    with open("./web/index.html", "r") as page:
        return self.html(page.read())


@app.page("/status")
async def get_status(self, request):
    """
    """
    with open("./web/status.html", "r") as page:
        return self.html(page.read())


def _get_if_in(item, dictn):
    """
    """
    for pair, match in dictn.items():
        if item in pair:
            return match

    return None


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
        with open(path, "w+") as kernel_file:
            kernel_file.write(f"- {self.number_of_edges()}\n")
            for (
                (matched_u, matched_v),
                (neighbours_u, neighbours_v),
            ) in self.matching.items():
                kernel_file.write(f"{matched_u} {matched_v}\n")
                for edge_u, edge_v in neighbours_u:
                    kernel_file.write(f"{edge_u} {edge_v}\n")
                for edge_u, edge_v in neighbours_v:
                    kernel_file.write(f"{edge_u} {edge_v}\n")

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


if __name__ == "__main__":
    app.main()
