import numpy as np
from settings import *
import networkx as nx

"""Uses a very simple fraction to generate the boost; num_winning_resources/total_allocated_to_bf"""
def simple_boost(blue_resources, red_resources):
    if red_resources < blue_resources:
        blue_factor = 1.5
        red_factor = 1
    else:
        blue_factor = 1
        red_factor = 1.5
    return blue_factor, red_factor

"""Uses logistic model to generate a boost"""
def logistic_boost(blue_resources, red_resources):
    if red_resources == 0 and blue_resources == 0:
        return 1, 1
    elif red_resources == 0:
        return 1 + MAX_BOOST, 1
    elif blue_resources == 0:
        return 1, 1+MAX_BOOST
    elif red_resources < blue_resources:
        frac = blue_resources/red_resources
        exp = -1 * STEEPNESS_K * (frac - 1.5)
        blue_factor = 1 + MAX_BOOST/(1+np.e**exp)
        red_factor = 1
    elif red_resources >= blue_resources:
        frac = red_resources/blue_resources
        exp = -1*STEEPNESS_K*(frac - 1.5)
        red_factor = 1 + MAX_BOOST/(1+np.e**exp)
        blue_factor = 1
    return blue_factor, red_factor

"""This function takes in user input"""
def get_user_input(num_battlefields=NUM_BATTLEFIELDS, autoplay=False):
    user_vals = []
    for i in range(0, NUM_BATTLEFIELDS):
        if not autoplay:
            usr_input = input("Enter value for battlefield " + str(i + 1) + ": ")
            try:
                usr_input = int(usr_input)
            except ValueError:
                print("Please enter a numeral. Quitting.")
                return
            user_vals.append(usr_input)
        else:
            user_vals.append(1)
    return user_vals

"""This file contains the code necessary to run one round of the game. If you want to run multiple rounds,
you have to keep calling run_game and giving it the battlefields."""
def run_game(battlefields, threshold, player1_vals=None, player2_vals=None, autoplay=False):
    #determine who won each battlefield
    if player1_vals is None:
        print("Provide input for player 1:")
        player1_vals = get_user_input()
    if player2_vals is None:
        print("Provide input for player 2:")
        player2_vals = get_user_input()

    polarizations = []
    for i in range(0, NUM_BATTLEFIELDS):
        new_colors = []
        if not autoplay:
            print("For Battlefield " + str(i+1) + " the blue player played " + str(player1_vals[i])
                  + " and the red player played " + str(player2_vals[i]) + "\n")
            blue_factor, red_factor = logistic_boost(player1_vals[i], player2_vals[i])
        else:
            blue_factor = 1
            red_factor = 1
        print("Red Factor", red_factor, "Blue Factor", blue_factor)

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
            if (percent_blue * blue_factor >= threshold) and (percent_red * red_factor < threshold):
                next_color = 'blue'
            elif (percent_red * red_factor >= threshold) and (percent_blue * blue_factor < threshold):
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

        print("Blue Nodes: " + str(total_blue))
        print("Red Nodes: " + str(total_red))
        print("\n")
        polarizations.append(total_blue/NUM_NODES)
    return polarizations