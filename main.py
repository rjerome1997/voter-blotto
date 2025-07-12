from create_nodes import *
from run_game import run_game


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
    run_game(battlefields, curr_threshold)
    for i in battlefields:
        print(i)
    curr_threshold = curr_threshold*RATE_OF_INCREASE


