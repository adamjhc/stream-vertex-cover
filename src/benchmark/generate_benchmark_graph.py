"""Usage: generate_benchmark_graph.py <benchmark_json>

Arguments:
    benchmark_json      The json file outputted from the benchmarking script

Options:
    -h --help           Show this screen
"""
import pyperf
from docopt import docopt
import matplotlib.pyplot as plt
from math import log2


def generate_benchmark_graph(json_file: str):
    suite = pyperf.BenchmarkSuite.load(json_file)

    stream_graphs, stream_edges, stream_k_values, stream_means, stream_stdevs = (
        [],
        [],
        [],
        [],
        [],
    )
    local_graphs, local_edges, local_k_values, local_means, local_stdevs = (
        [],
        [],
        [],
        [],
        [],
    )

    for benchmark in suite:
        domain, graph, edges, k = benchmark.get_name().split("-")
        mean = benchmark.mean()
        stdev = benchmark.stdev()

        if domain == "stream":
            stream_graphs.append(graph)
            stream_edges.append(int(edges))
            stream_k_values.append(int(k))
            stream_means.append(mean)
            stream_stdevs.append(stdev)
        elif domain == "local":
            local_graphs.append(graph)
            local_edges.append(int(edges))
            local_k_values.append(int(k))
            local_means.append(mean)
            local_stdevs.append(stdev)

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(12, 8), sharey=True)

    ax_left.scatter(
        stream_edges, stream_means, color="blue", label="Stream",
    )
    ax_left.scatter(
        local_edges, local_means, color="green", label="Local",
    )
    ax_left.set_xlabel("Edges")
    ax_left.set_ylabel("Time (s)")
    ax_left.set_xscale("log")

    ax_right.scatter(
        stream_k_values, stream_means, color="blue", label="Stream",
    )
    ax_right.scatter(
        local_k_values, local_means, color="green", label="Local",
    )
    ax_right.set_xlabel("k")
    ax_right.set_xscale("log")

    plt.yscale("log")

    fig.suptitle(json_file)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    args = docopt(__doc__)
    generate_benchmark_graph(args["<benchmark_json>"])
