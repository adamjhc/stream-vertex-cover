from pathlib import Path
from typing import Iterator, Optional

from faust import ChannelT, StreamT, TopicT
from terminaltables import SingleTable

from stream_models import GraphRequest, JobInfo


async def handle_branching(
    topic_requests: TopicT,
    stream_edges: StreamT,
    channel_edges: ChannelT,
    channel_results: ChannelT,
    job_no: str,
    job: JobInfo,
):
    """
    Handles the branching job type

    Parameters
    ----------
        topic_requests : TopicT
            Kafka "requests" topic to request edges from graph
        stream_edges : StreamT
            Faust stream of edges
        channel_edges : ChannelT
            Faust channel to pass edges to
        channel_results : ChannelT
            Faust channel to pass results to
        job_no : str
            Job number
        job : JobInfo
            Information of the job
    """
    vertex_cover = await _calculate_vertex_cover(
        topic_requests, stream_edges, channel_edges, job
    )

    # Create results table to display on frontend
    result = [
        ("Algorithm", job.algorithm),
        ("Graph Name", Path(job.path).stem),
        ("k", job.k),
        ("VC exists?", vertex_cover is not None),
    ]

    if vertex_cover is not None:
        result.extend(
            [("VC size", len(vertex_cover)),]
        )

    result_table = SingleTable(result, title=f"Job {job_no}")
    result_table.inner_heading_row_border = False

    # Results table is multi-line to write all lines to results channel
    for line in result_table.table.splitlines():
        await channel_results.put(line)


async def _calculate_vertex_cover(
    topic_requests: TopicT, stream_edges: StreamT, channel_edges: ChannelT, job: JobInfo
) -> Optional[set]:
    """
    Calculates a vertex cover of a given graph using a multi-pass branching
    method

    Parameters
    ----------
        topic_requests : TopicT
            Kafka "requests" topic to request edges from graph
        stream_edges : StreamT
            Faust stream of edges
        channel_edges : ChannelT
            Faust channel to pass edges to
        job : JobInfo
            Information of the job

    Returns
    -------
        Optional[set]
            Vertex cover if one exists else None
    """
    for bin_string in _get_binary_strings(job.k):

        vertex_cover: set = set()
        vertex_cover_exists = True
        bin_string_pos = 0

        async for edge in stream_edges:
            if edge.is_end:
                break

            if not vertex_cover_exists:
                continue

            await channel_edges.put(edge)

            u = edge.u
            v = edge.v

            if u not in vertex_cover and v not in vertex_cover:
                if bin_string_pos == job.k:
                    vertex_cover_exists = False
                    continue

                edge_sm, edge_bg = (u, v) if u < v else (v, u)

                if bin_string[bin_string_pos] == "0":
                    vertex_cover.add(edge_sm)
                else:
                    vertex_cover.add(edge_bg)

                bin_string_pos += 1

        if vertex_cover_exists:
            return vertex_cover

        # Request new stream of edges
        await topic_requests.send(value=GraphRequest(job.path))

    return None


def _get_binary_strings(k: int) -> Iterator[str]:
    """
    Generates binary strings up to a given length k

    Yields
    ------
        str
            Incrementing binary strings
    """
    for i in range(2 ** k):
        yield bin(i)[2:].rjust(k, "0")
