# Graph Batch Processing Pipeline

## [Taking this as a guide:](https://blog.syncsort.com/2019/07/big-data/streaming-data-pipelines-how-to-build-one/) 

To build a streaming data pipeline, we'll need a few tools.

First, you’ll require an in-memory framework (such as Spark), which handles batch, real-time analytics, and data processing workloads. You’ll also need a streaming platform (Kafka is a popular choice, but there are others on the market) to build the streaming data pipeline. In addition, you’ll also need a NoSQL database (many people use HBase, but you have a variety of choices available). 

Step three is to fetch the data from the streaming platform. Next, we'll process the data. The fifth step is to manage the pipeline to ensure everything is working as it’s supposed to. 

## In-Memory Framework

[Spark](https://spark.apache.org/)
