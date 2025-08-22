import networkx as nx
import json
from settings import *
from create_nodes import *
import pandas
import numpy as np

"""This file can be run by itself and it will create battlefields and run them in autoplay until they converge,
then output the data into a heatmap."""

def run_game(battlefield, threshold):
    user_vals = []
    computer_vals = []
    new_colors = []
    for node in battlefield.nodes:
        neighbors = battlefield.neighbors(node)
        num_blue_neighbors = 0
        num_red_neighbors = 0
        for neighbor in neighbors:
            neighbor_color = battlefield.nodes[neighbor]['color']
            if neighbor_color == 'blue':
                num_blue_neighbors += 1
            else:
                num_red_neighbors += 1
        percent_blue = num_blue_neighbors/(num_red_neighbors + num_blue_neighbors)
        percent_red = num_red_neighbors/(num_blue_neighbors+num_red_neighbors)
        if (percent_blue >= threshold) and (percent_red < threshold):
            next_color = 'blue'
        elif (percent_red >= threshold) and (percent_blue < threshold):
            next_color = 'red'
        else:
            next_color = battlefield.nodes[node]['color']
        new_colors.append(next_color)

    #set all the nodes to their next color
    j = 0
    total_blue = 0
    total_red = 0
    for node in battlefield.nodes:
        battlefield.nodes[node]['color'] = new_colors[j]
        if new_colors[j] == 'red':
            total_red += 1
        else:
            total_blue += 1
        j+=1
    #if it's entirely one color, record that color and states to convergence
    #we're doing that in the outer loop, so just return to number of red and blue
    return total_red, total_blue

"""AUTOMATING DATA COLLECTION"""
#create random graphs and record all their data
"""CREATE A RANDOM GRAPH AND RECORD DATA"""
battlefields = []
color = 0
#Okay, this is going to be a list of dicts indexed by the name of the feature. We should have a document that
#keeps track of what everything is named and what the names mean.
graph_data = []
#cycle through polarization
polarization = 0.45
for i in range(2000): #just generate ten graphs and make sure they're different
    if i % 100 == 0:
        print(i)
    #create the local dict to store all the graph data
    curr_data = {}
    #pick random number of nodes
    #num_nodes = random.randint(200,500)
    num_nodes = 300
    curr_data['num_nodes'] = num_nodes
    k = random.randint(5,15)
    curr_data['k'] = k
    p = random.random()
    curr_data['p'] = p
    battlefields.append(create_nodes(k=k, p=p, num_nodes=num_nodes))
    #set random polarizations
    curr_data['polarization'] = polarization
    color_nodes(battlefields[i], color,num_nodes=num_nodes, polarization=polarization)
    polarization += 0.01
    if polarization == 0.56:
        polarization = 0.45
    color = not color
    #Okay, now we've generated a graph, we need to print this information about it to see if it's changing.
    #num nodes and edges
    #print(battlefields[i])

    #num cycles
    """
    This is WAYYYY too large, it will always hang on it and run forever. 
    simple_cycles = nx.simple_cycles(battlefields[i], length_bound=100)
    num = 0
    for g in simple_cycles:
        num+=1
        if num >= 10000:
            break
    print(num)
    #print(len(simple_cycles))
    """
    #girth
    #print("Girth:", nx.girth(battlefields[i]))
    #why is the girth literally always three??

    #density
    #print("Density:", nx.density(battlefields[i]))
    curr_data['density'] = nx.density(battlefields[i])

    #diameter
    #print("Diameter:", nx.diameter(battlefields[i]))
    curr_data['diameter'] = nx.diameter(battlefields[i])

    #average path length?
    #print("Average Path Length:", nx.average_shortest_path_length(battlefields[i]))
    curr_data['avg_path_length'] = nx.average_shortest_path_length(battlefields[i])

    #clustering coefficient?
    #print("Clustering Coefficient:", nx.average_clustering(battlefields[i]))
    curr_data['avg_clustering'] = nx.average_clustering(battlefields[i])

    #average connectivity
    #print("Connectivity:", nx.average_node_connectivity(battlefields[i]))

    #number of nodes of degree delta and the color of those nodes
    highest_degree_node = max(battlefields[i].nodes, key=battlefields[i].degree)
    max_degree = battlefields[i].degree(highest_degree_node)

    #print(f"Degree of the highest degree node: {max_degree}")
    curr_data['max_degree'] = max_degree

    #print("Color of highest degree node:", battlefields[i].nodes[highest_degree_node]['color'])
    curr_data['max_degree_color'] = battlefields[i].nodes[highest_degree_node]['color']

    # Find all nodes with the highest degree
    node_degrees = dict(battlefields[i].degree())
    nodes_with_highest_degree = [node for node, degree in node_degrees.items() if degree == max_degree]
    num_red = 0; num_blue = 0
    for node in nodes_with_highest_degree:
        if battlefields[i].nodes[node]['color'] == 'red':
            num_red += 1
        else:
            num_blue += 1
    #print("The number of blue nodes of degree delta is", num_blue, "and the number of red is", num_red)
    curr_data['num_maximal_blue_nodes'] = num_blue
    curr_data['num_maximal_red_nodes'] = num_red

    #ten most connected nodes in the graph
    sorted_nodes = sorted(node_degrees.items(), key=lambda item: item[1], reverse=True)
    top_ten_nodes = sorted_nodes[:10]

    num_red = 0; num_blue = 0
    tot_blue_degree = 0; tot_red_degree = 0
    for node, degree in top_ten_nodes:
        if battlefields[i].nodes[node]['color'] == 'red':
            num_red += 1
            tot_red_degree += degree
        else:
            num_blue += 1
            tot_blue_degree += degree

    #print("Of the ten most connected nodes,", num_blue,"are blue and", num_red, "are red.")
    #print("The total red degree across the top ten is", tot_red_degree,"and the blue is", tot_blue_degree)
    curr_data['red_in_top_ten'] = num_red
    curr_data['blue_in_top_ten'] = num_blue
    curr_data['top_ten_red_degree'] = tot_red_degree
    curr_data['top_ten_blue_degree'] = tot_blue_degree

    #total red and blue degree in graph
    tot_blue_degree = 0; tot_red_degree = 0
    for node, degree in node_degrees.items():
        if battlefields[i].nodes[node]['color'] == 'red':
            num_red += 1
            tot_red_degree += degree
        else:
            num_blue += 1
            tot_blue_degree += degree
    #print("Total blue degree across entire graph:", tot_blue_degree)
    #print("Total red degree across entire graph:", tot_red_degree)
    curr_data['total_blue_degree'] = tot_blue_degree
    curr_data['total_red_degree'] = tot_red_degree

    #find clique number (size of maximal clique)
    #print(nx.node_clique_number(battlefields[i]))



    #run the simulation and record when it converges
    cont = True
    rounds = 0
    curr_threshold = THRESHOLD
    while cont:
        num_red, num_blue = run_game(battlefields[i], curr_threshold)
        curr_threshold = curr_threshold * RATE_OF_INCREASE
        if num_red == 300:
            curr_data['color'] = 'red'
            cont = False

        elif num_blue == 300:
            cont = False
            curr_data['color'] = 'blue'

        rounds += 1
        #check if we've exceeded reasonable number of rounds
        if rounds >= 100:
            cont = False

    curr_data['num_rounds'] = rounds

    graph_data.append(curr_data)

print(graph_data)

#record the data into data2.csv
print("Done collecting data")
with open("data_300_nodes.json", "w") as f:
    json.dump(graph_data, f, indent=4)