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
- GNU Make
- Docker (for using Kafka and Zookeeper)

### Instructions

1. Clone this repo
2. Run `pip install -r requirements.txt`
3. Enjoy!

### Demo

Run `make demo_local_stream`

## Backstory

This was my undergraduate final year project while studying at the University of Birmingham. Towards the end of the first term and through the December break I suffered from glandular fever for 6-7 weeks. Then, towards the end of the second term, we were hit with the COVID-19 pandemic. So, while there have been some bumps along the road, I'm glad this project has come to fruition.
