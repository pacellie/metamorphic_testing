from typing import Tuple
import pytest
from dijkstar import Graph, find_path  # type: ignore
from metamorphic_test import (
    transformation,
    metamorphic,
    system,
    relation,
    randomized,
)
from metamorphic_test.generators import RandInt


start_end = metamorphic("start_end")
random_cheap = metamorphic("random_cheap")


"""
This example demonstrates two MR test of a shortest path algorithm of an undirected graph.
- If the start and end nodes are swapped, the cost of the shortest path should remain the same.
- If an edge that is much cheaper than any other is added between two nodes / overwrites an
 existing edge, the cost of the shortest path should be less or equal than before.
"""


@transformation(start_end)
def switch_startend(graph: Graph, start: int, end: int) -> Tuple[Graph, int, int]:
    """Switch the starting and destination node from the tuple of pathfinder's inputs."""
    return graph, end, start


@transformation(random_cheap)
@randomized("newedge_start", RandInt(1, 4))
@randomized("newedge_end", RandInt(1, 4))
def add_random_cheap_edge(
    graph: Graph, start: int, end: int, newedge_start: int, newedge_end: int
) -> Tuple[Graph, int, int]:
    """Adds an edge that is much cheaper than any other / overwrites an
    existing edge with a much cheaper one."""
    graph_new = Graph(data=graph.get_data(), undirected=True)
    graph_new.add_edge(newedge_start, newedge_end, 1)
    return graph_new, start, end


@relation(start_end)
def cost_equal(x, y) -> bool:
    """Verifies that two paths has the same total cost."""
    return x.total_cost == y.total_cost


@relation(random_cheap)
def cost_greater_equal(x, y) -> bool:
    """Verifies that the first path has greater or equal total cost than the second one."""
    return x.total_cost >= y.total_cost


def vis_output(result) -> int:
    """The total cost of the path is the information that should be visualized."""
    return result.total_cost


# setup
graph1 = Graph(undirected=True)
graph1.add_edge(1, 2, 10)
graph1.add_edge(2, 3, 15)
graph1.add_edge(3, 4, 18)
graph2 = Graph(undirected=True)
graph2.add_edge(1, 2, 10)
graph2.add_edge(1, 3, 15)
graph2.add_edge(2, 4, 18)
graph2.add_edge(3, 4, 17)


@pytest.mark.parametrize("graph", [graph1, graph2])
@pytest.mark.parametrize("start", [2, 1])
@pytest.mark.parametrize("end", [4, 3])
@system(start_end, random_cheap, visualize_output=vis_output)
def test_add_pytest(graph: Graph, start: int, end: int):
    """Find a shortest path between two nodes in a graph"""
    return find_path(graph, start, end)
