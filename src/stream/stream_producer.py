import logging
from time import sleep

import faust
from faust import StreamT
from faust.web import Request, Response, View

from stream_models import Edge, GraphInfo

app = faust.App("producer", broker="kafka://localhost:9092", web_port=6067)

topic_requests = app.topic("requests", key_type=str, value_type=GraphInfo)
topic_info = app.topic("info", key_type=str, value_type=GraphInfo)
topic_edges = app.topic("edges", key_type=str, value_type=Edge)


@app.task()
async def on_started():
    logging.info("Ready")


@app.page("/request")
class WebProducer(View):
    async def post(self, request: Request) -> Response:
        body = await request.json()

        logging.info(f"Received {body['algorithm']} {body['graph']} {body['k']}")

        await send_graph(body["algorithm"], body["graph"], body["k"])

        return self.json({})


@app.agent(topic_requests)
async def stream(requests: StreamT[GraphInfo]):
    async for request in requests:
        send_graph(request.algorithm, request.path, request.k)


async def send_graph(algorithm, path, k):
    logging.info(f"Processing {algorithm} {path} {k}")

    with open(path, "r") as edgelist:
        await topic_info.send(value=GraphInfo(path, int(k)))

        for i, edge in enumerate(edgelist):
            u, v = edge.split()[:2]
            await topic_edges.send(key=str(i), value=Edge(u=u, v=v))

        await topic_edges.send(key=str(i + 1), value=Edge(is_end=True, u="-1", v="-1"))


if __name__ == "__main__":
    app.main()
