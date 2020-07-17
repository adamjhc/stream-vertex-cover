# Stream Vertex Cover

This project aims to provide implementations for parameterized streaming algorithms for vertex cover as posed in [Chitnis, Cormode, Hajiaghayi, & Monemizadeh, 2014](https://arxiv.org/abs/1405.0093) as well as to provide a basis for further work into parameterized streaming algorithms.

## Features

- Classical implementations for small graphs using [NetworkX](https://networkx.github.io/)
- Stream implementations using Python's [io](https://docs.python.org/3/library/io.html)
- Stream implementations using [Apache Kafka](https://kafka.apache.org/) and [Faust](http://faust.readthedocs.io/)
- Tools for visualising the algorithms
- Runtime analysis and memory profiling

## Code

All code has been statically type checked using [MyPy](http://mypy-lang.org/). View the docs [here](https://stream-vertex-cover.readthedocs.io/) or using the link above.

## Setup

### Requirements

- Python 3.8
- GNU Make (for running demos, alternatively run commands from Makefile manually)
- Docker and Docker Compose (for using Kafka and Zookeeper)
- [Imagemagick](https://imagemagick.org/) (for creating GIFs)

### Installation

1. Clone the repo

```sh
$ git clone https://github.com/adamjhc/stream-vertex-cover.git
```

2. (Optional) Create a python virtual environment
3. Install dependencies

```sh
$ pip install -r requirements.txt
```

### Demo

If everything has been setup correctly, you should be able to run the demo using

```sh
$ make demo_local_stream
python ./src/local_stream/local_stream.py branching-min ./src/test_sets/labelled_edge_lists/rome99.txt
┌Result────────┬────────┐
│ Graph Name   │ rome99 │
│ Graph Nodes  │ 3353   │
│ Graph Edges  │ 8870   │
│ Min k        │ 1458   │
│ Kernel Nodes │ 3353   │
│ Kernel Edges │ 8870   │
│ Reduction    │ 0.0%   │
└──────────────┴────────┘
```

## About

This was my final year project while studying BSc Computer Science at the University of Birmingham.

This project was supervised by [Rajesh Chitnis](https://rajeshchitnis.github.io/)
