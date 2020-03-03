def task_mypy():
    """Run mypy static type checking for entire project"""
    return {
        "actions": ["mypy --ignore-missing-imports %(targets)s "],
        "targets": [
            "src/local",
            "src/local_stream",
            "src/stream",
            "src/visuals",
            "src/utils",
        ],
        "verbosity": 2,
    }


def task_demo_local():
    """Demo Local capabilities"""
    return {"actions": []}


def task_demo_local_stream():
    """Demo Local-Stream capabilities"""
    # vc_stream.py branching FILE <k> [--log=LEVEL]
    # vc_stream.py kernel-exists FILE <k> [--log=LEVEL]
    # vc_stream.py kernel-br FILE <k> [--log=LEVEL]
    # vc_stream.py kernel-min FILE
    return {
        "actions": ["python ./src/local_stream/vc_stream.py %(task)s %(targets)s",],
        "params": [
            {
                "name": "task",
                "short": "t",
                "long": "task",
                "default": "kernel-min",
                "help": "Which task to run in local-stream",
            },
            {"name": "k", "short": "k", "default": "", "help": "k value to use"},
        ],
        "targets": ["./src/test_sets/stream/les_miserables.txt"],
        "verbosity": 2,
    }


def task_demo_visuals():
    """Demo visualisations"""
    # kernel_stream_demo.py <edge_list_file> <k> [--delay=DELAY --label]
    return {
        "actions": [
            "python ./src/visuals/kernel_stream_demo.py \
                ./src/test_sets/edge_lists/erdos_renyi_100_0.05_edgelist.txt \
                66 \
                --delay=0.01"
        ],
        "verbosity": 0,
    }

