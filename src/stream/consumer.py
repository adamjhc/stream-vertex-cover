import faust

app = faust.App("consumer", broker="kafka://localhost:9092", value_serializer="raw",)

topic_edges = app.topic("edges")


@app.agent(topic_edges)
async def process_edges(edges):
    async for edge in edges:
        print(edge)


@app.page("/")
async def get_index(self, request):
    with open("./web/index.html", "r") as page:
        return self.html(page.read())


@app.page("/status")
async def get_status(self, request):
    with open("./web/status.html", "r") as page:
        return self.html(page.read())


if __name__ == "__main__":
    app.main()
