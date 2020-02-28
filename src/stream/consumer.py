import faust

app = faust.App("hello-world", broker="kafka://localhost:9092", value_serializer="raw",)

greetings_topic = app.topic("greetings")


@app.agent(greetings_topic)
async def greet(greetings):
    async for greeting in greetings:
        print(greeting)


@app.page("/")
async def get_index(self, request):
    return self.html("<h1>Faust homepage</h1>")


if __name__ == "__main__":
    app.main()
