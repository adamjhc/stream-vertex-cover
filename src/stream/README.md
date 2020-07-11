# Stream

![Website](../../dissertation/images/stream.jpg)

This directory serves as a example of how these algorithms would be more typically implemented into a streaming framework such as Kafka. The website gives you options on the job you wish to process, this includes choosing the algorithm, graph, and a k value. On submit, you will see the edges of the graph stream down the middle column until the entire graph has been processed and a results table will appear in the right column.

In order to run Kafka, ZooKeeper is also needed so a docker-compose file has been provided for ease of use.

## Steps to run

1. `$ docker-compose up -d`
2. `$ python stream_producer.py worker -l info`

In another terminal

3. `$ python stream.py worker -l info`
4. Visit http://localhost:6066

### To shutdown

1. Ctrl+C to exit python programs
2. `$ docker-compose down`
