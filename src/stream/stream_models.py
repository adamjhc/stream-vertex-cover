import faust


class Edge(faust.Record):
    """
    Faust record that holds edge information
    """

    u: str
    v: str
    is_end: bool = False


class JobInfo(faust.Record):
    """
    Faust record that holds job information
    """

    algorithm: str
    path: str
    k: int


class GraphRequest(faust.Record):
    """
    Faust record that holds graph request information
    """

    path: str
