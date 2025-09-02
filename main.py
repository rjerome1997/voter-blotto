from create_nodes import *
from run_game import run_game
import math

def random_model(resources = RESOURCES, num_battlefields = NUM_BATTLEFIELDS, autoplay=False):
    if autoplay:
        return [1] * num_battlefields
    rand_n = [random.random() for i in range(num_battlefields)] #generate a random value for each battlefield
    result = [math.floor(i*resources/sum(rand_n)) for i in rand_n] #divide each value by sum*resources to get floats that add to resources and then floor to get integers
    #make up for flooring by adding 1 to random values until you get to sum = resources
    for i in range(resources - sum(result)):
        result[random.randint(0,num_battlefields-1)] += 1
    return result

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

#run the simulation
curr_threshold = THRESHOLD
for i in range(0, NUM_ROUNDS):
    print("ROUND " + str(i+1))
    #just run the random model against the user
    player1_vals = random_model()
    run_game(battlefields, curr_threshold, player1_vals=None)
    for i in battlefields:
        print(i)
    curr_threshold = curr_threshold*RATE_OF_INCREASE


