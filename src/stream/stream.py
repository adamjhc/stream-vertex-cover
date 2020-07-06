import logging

import faust
from aiohttp_sse import sse_response
from faust import StreamT

from stream_kernel import handle_kernel
from stream_branching import handle_branching
from stream_models import Edge, JobInfo

web_port = 6066

app = faust.App("kernelizer", broker="kafka://localhost:9092", web_port=web_port)
app.web.add_static("/static/", path="./static")


topic_edges = app.topic("edges", key_type=str, value_type=Edge)
topic_info = app.topic("info", key_type=str, value_type=JobInfo)

channel_edges = app.channel()
channel_results = app.channel()


@app.task()
async def on_started():
    """
    """
    logging.info(f"Visit http://localhost:{web_port}")


@app.agent(topic_info)
async def handle_jobs(stream_jobs: StreamT[Edge]):
    """
    """
    stream_edges = app.stream(topic_edges)

    async for job_no, job in stream_jobs.items():
        logging.info(f"Job #{job_no} {job.algorithm} {job.path} {job.k}")

        if job.algorithm == "kernel":
            await handle_kernel(
                stream_edges, channel_edges, channel_results, job_no, job
            )
        elif job.algorithm == "branching":
            await handle_branching()


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


if __name__ == "__main__":
    app.main()