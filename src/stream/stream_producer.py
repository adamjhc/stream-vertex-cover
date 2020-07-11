import logging

import faust
from faust import StreamT
from faust.web import Request, Response, View

from stream_models import Edge, GraphRequest, JobInfo

app = faust.App("graph-producer", broker="kafka://localhost:9092", web_port=6067)

# Kafka topic for streaming job information along
topic_info = app.topic("info", key_type=str, value_type=JobInfo)

# Kafka topic for streaming edges along
topic_edges = app.topic("edges", key_type=str, value_type=Edge)

# Kafka topic for streaming graph requests
topic_requests = app.topic("requests", key_type=str, value_type=GraphRequest)


# Job number counter
job_no = 1


@app.task()
async def on_started():
    """
    Logs "Ready" on start
    """
    logging.info("Ready")


@app.page("/request")
class WebProducer(View):
    async def post(self, request: Request) -> Response:
        """
        Handles HTTP POST "/request"

        Creates new job and sends edges for processing

        Parameters
        ----------
            request : Request
                Incoming web request

        Returns
        -------
            Response
                Empty HTTP 200 json response
        """
        body = await request.json()

        await send_job(job_no, body["algorithm"], body["graph"], int(body["k"]))

        return self.json({})


@app.agent(topic_requests)
async def handle_graph_requests(requests: StreamT[GraphRequest]):
    """
    Faust agent that handles requests stream, sends new stream of graph edges

    Parameters
    ----------
        requests : StreamT[GraphRequest]
            Incoming graph request
    """
    async for request in requests:
        await send_edges(request.path)


async def send_job(job_no: int, algorithm: str, path: str, k: int):
    """
    Sends job and edges for processing. Increments job counter

    Parameters
    ----------
        job_no : int
            Job number
        algorithm : str
            Name of algorithm
        path : str
            Path to graph edgelist
        k : str
            k value
    """
    logging.info(f"Job #{job_no} {algorithm} {path} {k}")

    await topic_info.send(key=str(job_no), value=JobInfo(algorithm, path, k))

    await send_edges(path)

    job_no += 1


async def send_edges(path: str):
    """
    Sends edges for processing

    Parameters
    ----------
        path : str
            Path to graph edgelist
    """
    with open(path, "r") as edgelist:
        for i, edge in enumerate(edgelist):
            u, v = edge.split()[:2]
            await topic_edges.send(key=str(i), value=Edge(u=u, v=v))

        # Send "end" edge to mark end of graph edges
        await topic_edges.send(key=str(i + 1), value=Edge(u="", v="", is_end=True))


if __name__ == "__main__":
    # Start Faust
    app.main()
