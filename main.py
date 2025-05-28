import networkx as nx
import matplotlib.pyplot as plt
from settings import *
from create_nodes import *
import random

def run_game(battlefields, threshold, autoplay=False):
    user_vals = []
    computer_vals = []
    for i in range(0, NUM_BATTLEFIELDS):
        if not autoplay:
            usr_input = input("Enter value for battlefield " + str(i+1) + ": ")
            try:
                usr_input = int(usr_input)
            except ValueError:
                print("Please enter a numeral. Quitting.")
                return
            user_vals.append(usr_input)
            #generate computer input, make sure the total will sum to RESOURCES
            computer_vals.append(random.randint(0,(RESOURCES - sum(computer_vals))))
        else:
            user_vals.append(1)
            computer_vals.append(1)

    #determine who won each battlefield
    for i in range(0, NUM_BATTLEFIELDS):
        new_colors = []
        if not autoplay:
            print("For Battlefield " + str(i+1) + " the user played " + str(user_vals[i])
                  + " and the computer played " + str(computer_vals[i]) + "\n")
            #blue_factor = user_vals[i] / 2 * (user_vals[i] + computer_vals[i]) + 1
            #red_factor = computer_vals[i] / 2 * (user_vals[i] + computer_vals[i]) + 1
            if user_vals[i] > computer_vals[i]:
                print("Blue wins battlefield " + str(i))
                blue_factor = 1.5
                red_factor = 1
            else:
                print("Red wins battlefield " + str(i))
                blue_factor = 1
                red_factor = 1.5

        else:
            blue_factor = 1
            red_factor = 1

        #modify the nodes and set their upcoming color
        for node in battlefields[i].nodes:
            neighbors = battlefields[i].neighbors(node)
            num_blue_neighbors = 0
            num_red_neighbors = 0
            for neighbor in neighbors:
                neighbor_color = battlefields[i].nodes[neighbor]['color']
                if neighbor_color == 'blue':
                    num_blue_neighbors += 1
                else:
                    num_red_neighbors += 1
            percent_blue = num_blue_neighbors/(num_red_neighbors + num_blue_neighbors)
            percent_red = num_red_neighbors/(num_blue_neighbors+num_red_neighbors)
            if percent_blue*blue_factor >= threshold:
                next_color = 'blue'
            elif percent_red*red_factor >= threshold:
                next_color = 'red'
            else:
                next_color = battlefields[i].nodes[node]['color']
            new_colors.append(next_color)

        #set all the nodes to their next color
        j = 0
        total_blue = 0
        total_red = 0
        for node in battlefields[i].nodes:
            battlefields[i].nodes[node]['color'] = new_colors[j]
            if new_colors[j] == 'red':
                total_red += 1
            else:
                total_blue += 1
            j+=1

        print("Red Nodes: " + str(total_red))
        print("Blue Nodes: " + str(total_blue))
        pos = nx.circular_layout(battlefields[i])
        nx.draw(battlefields[i], with_labels=True, node_color=new_colors)
        plt.show()

battlefields = []
#create nodes for node network and apportion into battlefields
color = 0
for i in range(0, NUM_BATTLEFIELDS):
    battlefields.append(create_nodes())
    color_nodes(battlefields[i], color)
    color = not color

print("STARTING NETWORK")
for i in battlefields:
    print(i)

#run the simulation in autoplay
curr_threshold = THRESHOLD
for i in range(0, NUM_ROUNDS):
    print("ROUND " + str(i+1))
    run_game(battlefields, curr_threshold, False)
    for i in battlefields:
        print(i)
    curr_threshold = curr_threshold*RATE_OF_INCREASE
