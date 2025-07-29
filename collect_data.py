from settings import *
from create_nodes import *
import pandas
import numpy as np

"""This file can be run by itself and it will create battlefields and run them in autoplay until they converge,
then output the data into a heatmap."""

def collect_data(battlefields, threshold):
    user_vals = []
    computer_vals = []
    for i in range(0, NUM_BATTLEFIELDS):
        user_vals.append(1)
        computer_vals.append(1)

    #determine who won each battlefield
    for i in range(0, NUM_BATTLEFIELDS):
        new_colors = []
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
            if (percent_blue*blue_factor >= threshold) and (percent_red*red_factor < threshold):
                next_color = 'blue'
            elif (percent_red*red_factor >= threshold) and (percent_blue*blue_factor < threshold):
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
        #if it's entirely one color, record that color and states to convergence
        #we're doing that in the outer loop, so just return to number of red and blue
        return total_red, total_blue

"""AUTOMATING DATA COLLECTION"""
#create pandas dataframe that will be indexed by polarization and degree and contain the num states
red_dummy_data = np.zeros((45, 99))
blue_dummy_data = np.zeros((45, 99))
row_names = []
for i in range(5, 50):
    row_names.append(str(i))
col_names = []
for i in range(1, 100):
    col_names.append(str(i))
red_df = pandas.DataFrame(red_dummy_data, index=row_names, columns=col_names)
blue_df = pandas.DataFrame(blue_dummy_data, index=row_names, columns=col_names)

#create a new map for every polarization/degree combination
curr_threshold = THRESHOLD
for avg_degree in range(5, 50):
    print(avg_degree)
    for polarization in range(1, 100):
        battlefields = []
        # create nodes for node network and apportion into battlefields
        color = 0
        for i in range(0, NUM_BATTLEFIELDS):
            battlefields.append(create_nodes(avg_degree))
            color_nodes(battlefields[i], color, polarization/100.0)
            color = not color

        """Check how many red nodes to make sure polarization is working (it is)
        num_red = 0
        for node, data in battlefields[0].nodes(data=True):
            if data['color'] == 'red':
                num_red += 1
        print("RED  " + str(num_red))
        """

        #run the simulation and record when it converges
        cont = True
        rounds = 1
        while cont:
            num_red, num_blue = collect_data(battlefields, curr_threshold)
            curr_threshold = curr_threshold * RATE_OF_INCREASE
            if num_red == NUM_NODES:
                cont = False
                #I want to put this in a pandas dataframe now...
                red_df.at[str(avg_degree), str(polarization)] = rounds

            elif num_blue == NUM_NODES:
                cont = False
                blue_df.at[str(avg_degree), str(polarization)] = rounds

            rounds += 1
            #check if we've exceeded reasonable number of rounds
            if rounds >= 100:
                print("Fail to converge " + str(polarization))
                cont = False

print(red_df.columns)
print(red_df.index)



red_df.to_csv("red_data.csv")
blue_df.to_csv("blue_data.csv")
