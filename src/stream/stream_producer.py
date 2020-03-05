import faust
from faust import StreamT
from time import sleep

from stream_models import Edge, GraphInfo

app = faust.App("producer", broker="kafka://localhost:9092", web_port=6067)

topic_requests = app.topic("requests", key_type=str, value_type=GraphInfo)
topic_info = app.topic("info", key_type=str, value_type=GraphInfo)
topic_edges = app.topic("edges", key_type=str, value_type=Edge)


@app.agent(topic_requests)
async def stream(requests: StreamT[GraphInfo]):
    async for request in requests:
        print(f"{request.path} {request.k}")
        await topic_info.send(value=request)

        with open(request.path, "r") as edgelist:
            for i, edge in enumerate(edgelist):
                u, v = edge.split()[:2]
                await topic_edges.send(key=str(i), value=Edge(u=u, v=v))

            await topic_edges.send(
                key=str(i + 1), value=Edge(is_end=True, u="-1", v="-1")
            )


if __name__ == "__main__":
    app.main()
