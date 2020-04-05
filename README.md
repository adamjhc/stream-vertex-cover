# Stream Vertex Cover

This project aims to provide implementations for parameterized streaming algorithms for vertex cover as posed in [Chitnis, Cormode, Hajiaghayi, & Monemizadeh, 2014](https://arxiv.org/abs/1405.0093) as well as to provide a basis for further work into parameterized streaming algorithms.

In this project you will find

- Basic implementations for small graphs using [NetworkX](https://networkx.github.io/)
- Stream implementations using Python `IO`
- Stream implementations using [Apache Kafka](https://kafka.apache.org/) and [Faust](http://faust.readthedocs.io/)
- Visualisations of algorithms
- Runtime analysis and memory profiling

All code is statically type checked using [MyPy](http://mypy-lang.org/). View the [docs](https://stream-vertex-cover.readthedocs.io/)

## Setup

### Requirements

- Python 3.8
- GNU Make (for running demos, alternatively run commands from Makefile manually)
- Docker and Docker Compose (for using Kafka and Zookeeper)

### Instructions

In a terminal:

1. Run `git clone https://github.com/adamjhc/stream-vertex-cover.git`
2. Run `cd stream-vertex-cover`
3. (Optional) Create a python virtual environment
4. Run `pip install -r requirements.txt`

### Demo

If everything has been setup correctly, you should be able to run the demo using

```sh
make demo_local_stream
````
