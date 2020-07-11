import logging

import faust
from aiohttp_sse import sse_response
from faust import StreamT

from stream_branching import handle_branching
from stream_kernel import handle_kernelization
from stream_models import Edge, GraphRequest, JobInfo

web_port = 6066

app = faust.App(
    "stream-vertex-cover", broker="kafka://localhost:9092", web_port=web_port
)

# Creates a static route on the web server
app.web.add_static("/static/", path="./static")

# Kafka topic for streaming job information along
topic_info = app.topic("info", key_type=str, value_type=JobInfo)

# Kafka topic for streaming edges along
topic_edges = app.topic("edges", key_type=str, value_type=Edge)

# Kafka topic for streaming graph requests
topic_requests = app.topic("requests", key_type=str, value_type=GraphRequest)

# Faust channel for inter-process communication for edges
channel_edges = app.channel()

# Faust channel for inter-process communication for results
channel_results = app.channel()


@app.task()
async def on_started():
    """
    Logs website to visit on start-up
    """
    logging.info(f"Visit http://localhost:{web_port}")


@app.agent(topic_info)
async def handle_jobs(stream_jobs: StreamT[Edge]):
    """
    Faust agent that handles stream of jobs and redirects to function depending on
    job type
    """
    stream_edges = app.stream(topic_edges)

    async for job_no, job in stream_jobs.items():
        logging.info(f"Job #{job_no} {job.algorithm} {job.path} {job.k}")

        if job.algorithm == "kernelization":
            await handle_kernelization(
                stream_edges, channel_edges, channel_results, job_no, job
            )
        elif job.algorithm == "branching":
            await handle_branching(
                topic_requests,
                stream_edges,
                channel_edges,
                channel_results,
                job_no,
                job,
            )


@app.page("/")
async def get_index(self, request):
    """
    Handles HTTP Get "/"

    Returns index page as html
    """
    with open("./pages/index.html", "r") as page:
        return self.html(page.read())


@app.page("/stream")
async def get_stream(self, request):
    """
    Handles HTTP Get "/stream"

    Creates a Server Side Event response to send edges in real time
    """
    async with sse_response(request) as response:
        async for edge in channel_edges:
            await response.send(f"{edge.u} {edge.v}")


@app.page("/results")
async def get_results(self, request):
    """
    Handles HTTP Get "/results"

    Creates a Server Side Event response to send results in real time
    """
    async with sse_response(request) as response:
        async for result in channel_results:
            await response.send(result)


if __name__ == "__main__":
    # Start Faust
    app.main()
