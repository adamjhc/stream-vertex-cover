import faust
from faust.cli import argument

from stream_models import GraphInfo

app = faust.App("sender", broker="kafka://localhost:9092", web_port=6068)

topic_requests = app.topic("requests", key_type=str, value_type=GraphInfo)


@app.command(argument("path"), argument("k"))
async def request(self, path, k):
    await topic_requests.send(value=GraphInfo(path, int(k)))


if __name__ == "__main__":
    app.main()
