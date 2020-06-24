import logging
import os
import signal

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
    print(f"Visit http://localhost:{web_port}")


@app.agent(topic_edges)
async def process_edges(edges: StreamT[Edge]):
    graphs = app.stream(topic_info)

    async for graph in graphs:
        matching: dict = {}
        kernel_exists = True

        async for i, edge in edges.enumerate(start=0):
            if edge.is_end:
                break

            if kernel_exists == False:
                continue

            is_neighbour = False

            match = _get_if_in(edge.u, matching)
            if match is not None and len(match.neighbours_u) <= graph.k:
                match.neighbours_u.append((edge.u, edge.v))
                is_neighbour = True

            match = _get_if_in(edge.v, matching)
            if match is not None and len(match.neighbours_v) <= graph.k:
                match.neighbours_v.append((edge.u, edge.v))
                is_neighbour = True

            if not is_neighbour:
                matching[(edge.u, edge.v)] = Match()

                if len(matching) > graph.k:
                    kernel_exists = False

        result_table = SingleTable(
            [
                ("Graph", "k", "Edges", "Kernel exists?"),
                (graph.path, graph.k, i, kernel_exists),
            ],
            title="Result",
        )
        logging.warning(f"Completed kernel\n{result_table.table}")


@app.page("/")
async def get_index(self, request):
    with open("./web/index.html", "r") as page:
        return self.html(page.read())


@app.page("/status")
async def get_status(self, request):
    with open("./web/status.html", "r") as page:
        return self.html(page.read())


def _get_if_in(item, dictn):
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


if __name__ == "__main__":
    app.main()
