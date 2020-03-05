import faust


class Edge(faust.Record):
    u: str
    v: str
    is_end: bool = False


class GraphInfo(faust.Record):
    path: str
    k: int
