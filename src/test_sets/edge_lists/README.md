# Edge lists

This directory contains Edge lists which are able to be imported into NetworkX. These follow the format of:

```text
u v
u v
u v
...
```

These can be imported into NetworkX using the `read_edgelist` function. They can also be used as a stream source where each line is a message. This mimics a more realistic situation of an unbounded stream since it's not possible to have information on the graph beforehand (in contrast to [labelled edge lists](../labelled_edge_lists/)).
