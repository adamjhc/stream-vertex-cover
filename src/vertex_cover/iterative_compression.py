"""
1-pass streaming algorithm for 𝑘-VC using O(𝑘^2⋅log⁡𝑛) bits
"""
from networkx import Graph


def vertex_cover_iterative_compression(graph: Graph, k: int) -> set:
    """
    Finds a vertex cover of at most size k using iterative compression

    Parameters
    ----------
        graph : Graph
            The graph to find a vertex cover of
        k : int
            Size k

    Returns
    -------
        set
            Vertex cover if one exists otherwise None
    """
    #  1: Find a maximal matching M (upto size k) in 1 pass which saturates the vertices VM
    #  2: If |M| exceeds k, then return NO and abort
    #  3: Let S = VM
    #  4: for i = |VM| to k + 1 do
    #  5: Y = ∅
    #  6: while Y ∈ Sk, Y 6= ♠ do
    #  7: if |{x ∈ V \ S : ∃y ∈ S \ Y s.t. {x, y} ∈ E(G)}| ≤ k − |Y | then
    #  8: S ← Y ∪ {x ∈ V \ S : ∃y ∈ S \ Y s.t. x − y ∈ E(G)} . Requires a pass through the data
    #  9: Break . Found a solution, and reduce value of i by 1
    # 10: else
    # 11: Y ← DictSk(Next(Y )) . Try the next subset
    # 12: if Y = ♠ then
    # 13: Return NO and abort
    # 14: if i = k then
    # 15: Return S
    pass
