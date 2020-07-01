import asyncio
import json
import logging
import os
import signal
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import faust
from aiohttp_sse import sse_response
from faust import StreamT
from faust.web.drivers.aiohttp import Web
from terminaltables import SingleTable

from stream_models import Edge, GraphInfo

web_port = 6066

app = faust.App("kernelizer", broker="kafka://localhost:9092", web_port=web_port)
app.web.add_static("/static/", path="./static")


topic_edges = app.topic("edges", key_type=str, value_type=Edge)
topic_info = app.topic("info", key_type=str, value_type=GraphInfo)

channel_edges = app.channel()
channel_results = app.channel()


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
        logging.info(f"Processing {graph.path} {graph.k}")

        kernel = Kernel(graph.k)
        kernel_exists = True

        async for i, edge in edges.enumerate(start=0):
            if edge.is_end:
                break

            if kernel_exists == False:
                continue

            await channel_edges.put(edge)

            if not kernel.next(edge.u, edge.v):
                kernel_exists = False

        graph_edges = i
        kernel_edges = kernel.number_of_edges()

        result_table = SingleTable(
            [
                ("Graph Name", Path(graph.path).stem),
                ("Graph Edges", graph_edges),
                ("k", graph.k),
                ("Kernel exists?", kernel_exists),
                ("Kernel Edges", kernel_edges),
                (
                    "Reduction",
                    f"{round(100 - ((kernel_edges / graph_edges) * 100), 2)}%",
                ),
            ],
            title="Result",
        )

        for line in result_table.table.splitlines():
            await channel_results.put(line)


@app.page("/")
async def get_index(self, request):
    """
    """
    with open("./views/index.html", "r") as page:
        return self.html(page.read())


@app.page("/stream")
async def get_stream(self, request):
    """
    """
    async with sse_response(request) as response:
        async for edge in channel_edges:
            await response.send(f"{edge.u} {edge.v}")


@app.page("/results")
async def get_results(self, request):
    """
    """
    async with sse_response(request) as response:
        async for result in channel_results:
            await response.send(result)


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
    app.main()
