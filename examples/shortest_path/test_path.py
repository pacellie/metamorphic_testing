import pytest

from dijkstar import Graph, find_path

from metamorphic_test import (
    transformation,
    metamorphic,
    system, relation, randomized,
)
from metamorphic_test.generators import RandInt


start_end = metamorphic('start_end')
random_cheap = metamorphic('random_cheap')


@transformation(start_end)
def switch_startend(graph, start, end):
    return graph, end, start


@transformation(random_cheap)
@randomized('newedge_start', RandInt(1, 4))
@randomized('newedge_end', RandInt(1, 4))
def add_random_cheap_edge(graph, start, end, newedge_start, newedge_end):
    graph_new = Graph(data=graph.get_data(), undirected=True)
    graph_new.add_edge(newedge_start, newedge_end, 1)
    return graph_new, start, end


@relation(start_end)
def cost_equal(x, y):
    return x.total_cost == y.total_cost


@relation(random_cheap)
def cost_greater_equal(x, y):
    return x.total_cost >= y.total_cost


def vis_output(result):
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
def test_add_pytest(graph, start, end):
    return find_path(graph, start, end)
