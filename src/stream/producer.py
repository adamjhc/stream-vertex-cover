import faust
from faust.cli import argument
from time import sleep
import click

app = faust.App(
    "producer", broker="kafka://localhost:9092", value_serializer="raw", web_port=6067
)


@app.command(
    argument("edgelist", type=click.File("r")), argument("topic_name", type=str)
)
async def send(self, edgelist, topic_name):
    topic = app.topic(topic_name)
    for edge in edgelist:
        await topic.send(value=edge)


if __name__ == "__main__":
    app.main()