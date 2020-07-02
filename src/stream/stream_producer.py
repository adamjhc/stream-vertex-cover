import logging
from time import sleep

import faust
from faust import StreamT
from faust.web import Request, Response, View

from stream_models import Edge, JobInfo

app = faust.App("producer", broker="kafka://localhost:9092", web_port=6067)

topic_requests = app.topic("requests", key_type=str, value_type=JobInfo)
topic_info = app.topic("info", key_type=str, value_type=JobInfo)
topic_edges = app.topic("edges", key_type=str, value_type=Edge)

job_no = 1


@app.task()
async def on_started():
    logging.info("Ready")


@app.page("/request")
class WebProducer(View):
    async def post(self, request: Request) -> Response:
        body = await request.json()

        await send_job(body["algorithm"], body["graph"], body["k"])

        return self.json({})


@app.agent(topic_requests)
async def stream(requests: StreamT[JobInfo]):
    async for request in requests:
        send_job(request.algorithm, request.path, request.k)


async def send_job(algorithm, path, k):
    global job_no

    logging.info(f"Job #{job_no} {algorithm} {path} {k}")

    with open(path, "r") as edgelist:
        await topic_info.send(key=str(job_no), value=JobInfo(algorithm, path, int(k)))
        job_no += 1

        for i, edge in enumerate(edgelist):
            u, v = edge.split()[:2]
            await topic_edges.send(key=str(i), value=Edge(u=u, v=v))

        await topic_edges.send(key=str(i + 1), value=Edge(is_end=True, u="-1", v="-1"))


if __name__ == "__main__":
    app.main()
