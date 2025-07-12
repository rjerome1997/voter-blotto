import networkx as nx
import matplotlib.pyplot as plt
import random

from networkx.generators.degree_seq import expected_degree_graph

from settings import *

def create_nodes(k = WATTS_STROGATZ_K, p = WATTS_STROGATZ_P):
    max_iters = 1000 #maximum attempts to create desired graph
    for _ in range(max_iters):
        try:
            w = []
            for i in range(NUM_NODES):
                w.append(random.randint(10,15))
            graph = nx.watts_strogatz_graph(NUM_NODES, WATTS_STROGATZ_K, WATTS_STROGATZ_P)
            return graph
        except nx.NetworkXError as e:
            print(f"Attempt failed: {e}")
            continue
    return

def color_nodes(graph, color, polarization = POLARIZATION):
    num_to_color = int(NUM_NODES*polarization)
    if color == 0:
        color = 'blue'
        default = 'red'
    else:
        color = 'red'
        default = 'blue'
    nodes = list(graph.nodes())
    nodes_to_color = random.sample(nodes, num_to_color)

    #assign random nodes
    for node in nodes_to_color:
        graph.nodes[node]['color'] = color

    #assign the rest of the nodes the opposite color
    for node in nodes:
        if 'color' not in graph.nodes[node]:
            graph.nodes[node]['color'] = default

    #create list of colors to pass to drawing
    node_colors = [graph.nodes[node]['color'] for node in nodes]

"""
    plt.figure(figsize=(10,10))
    pos = nx.circular_layout(graph)
    nx.draw(graph, with_labels=True, node_color = node_colors)
    plt.show()
"""
