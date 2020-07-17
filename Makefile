.DEFAULT_GOAL := list

list:
	@echo "list			Show this list of actions"
	@echo "mypy			Run mypy static type checking for entire project"
	@echo "demo_local_stream	Demo Local-Stream capabilities"
	@echo "demo_visuals		Demo visualisations"

mypy:
	mypy ./src/local ./src/local_stream ./src/stream ./src/visuals ./src/utils

demo_local_stream:
	python ./src/local_stream/local_stream.py branching-min ./src/test_sets/labelled_edge_lists/florentine_families_labelled.txt

demo_visuals:
	python ./src/visuals/kernel_stream_demo.py ./src/test_sets/edge_lists/erdos_renyi_100_0.05_edgelist.txt 66 --delay=0.01
