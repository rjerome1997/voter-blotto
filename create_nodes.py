import networkx as nx
import matplotlib.pyplot as plt
import random

from networkx.generators.degree_seq import expected_degree_graph

from settings import *

def create_nodes():
    max_iters = 1000 #maximum attempts to create desired graph
    for _ in range(max_iters):
        try:
            w = []
            for i in range(NUM_NODES):
                w.append(random.randint(10,15))
            #graph = expected_degree_graph(w, None, False)
            #n = 10, k = 4, p = 0.5
            graph = nx.watts_strogatz_graph(NUM_NODES, 12, 0.5)
            # Check if the generated graph has a total degree in the proper range
            total_degree = 2*graph.number_of_edges()
            #if NUM_NODES*LOW_AVG <= total_degree <= NUM_NODES*HIGH_AVG:
                #check if max and min are no violated:
             #   if min(dict(graph.degree()).values()) >= MINIMUM_DEGREE and max(dict(graph.degree()).values()) <= MAX_DEGREE:
              #      return graph
            return graph
        except nx.NetworkXError as e:
            print(f"Attempt failed: {e}")
            continue
    return

def color_nodes(graph, color):
    num_to_color = int(NUM_NODES*POLARIZATION)
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

    plt.figure(figsize=(10,10))
    pos = nx.circular_layout(graph)
    nx.draw(graph, with_labels=True, node_color = node_colors)
    plt.show()

