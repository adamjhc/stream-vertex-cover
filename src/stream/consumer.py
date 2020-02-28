import faust

app = faust.App("consumer", broker="kafka://localhost:9092", value_serializer="raw",)

greetings_topic = app.topic("greetings")


@app.agent(greetings_topic)
async def greet(greetings):
    async for greeting in greetings:
        print(greeting)


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
