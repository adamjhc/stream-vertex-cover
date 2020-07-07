import faust


class Edge(faust.Record):
    u: str
    v: str
    is_end: bool = False


class JobInfo(faust.Record):
    algorithm: str
    path: str
    k: int


class GraphRequest(faust.Record):
    path: str
