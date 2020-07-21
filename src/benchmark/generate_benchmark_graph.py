"""Usage: generate_benchmark_graph.py <benchmark_json>

Arguments:
    benchmark_json      The json file outputted from the benchmarking script

Options:
    -h --help           Show this screen
"""
import pyperf
from docopt import docopt
import matplotlib.pyplot as plt


def generate_benchmark_graph(json_file: str):
    suite = pyperf.BenchmarkSuite.load(json_file)

    stream_graphs, stream_k_values, stream_means, stream_stdevs = [], [], [], []
    local_graphs, local_k_values, local_means, local_stdevs = [], [], [], []

    for benchmark in suite:
        domain, graph, k = benchmark.get_name().split("-")
        mean = benchmark.mean()
        stdev = benchmark.stdev()

        if domain == "stream":
            stream_graphs.append(graph)
            stream_k_values.append(k)
            stream_means.append(mean)
            stream_stdevs.append(stdev)
        elif domain == "local":
            local_graphs.append(graph)
            local_k_values.append(k)
            local_means.append(mean)
            local_stdevs.append(stdev)

    plt.figure(figsize=(6, 8))
    plt.errorbar(
        stream_k_values,
        stream_means,
        stream_stdevs,
        fmt="o",
        color="blue",
        label="Stream",
    )
    plt.errorbar(
        local_k_values, local_means, local_stdevs, fmt="o", color="green", label="Local"
    )
    plt.xlabel("k")
    plt.ylabel("Time (s)")
    plt.yscale("log")
    plt.title(json_file)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    args = docopt(__doc__)
    generate_benchmark_graph(args["<benchmark_json>"])
