from run_game import *
from create_nodes import *
import pandas as pd
import math

#load combined_df csv
red_df = pd.read_csv('data/red_data.csv')
blue_df = pd.read_csv('data/blue_data.csv')

"""Generates computer move (random numbers)"""
def random_model(features, resources = RESOURCES, num_battlefields = NUM_BATTLEFIELDS, autoplay=False):
    if autoplay:
        return [1] * num_battlefields
    rand_n = [random.random() for i in range(num_battlefields)] #generate a random value for each battlefield
    result = [math.floor(i*resources/sum(rand_n)) for i in rand_n] #divide each value by sum*resources to get floats that add to resources and then floor to get integers
    #make up for flooring by adding 1 to random values until you get to sum = resources
    for i in range(resources - sum(result)):
        result[random.randint(0,num_battlefields-1)] += 1
    return result

def deterministic_model(features):
    #generate NUM_BATTLEFIELDS length list of integers that sums to resources
    vals = []
    for polarization, degree in features:
        if polarization == 100 or polarization == 0:
            vals.append(0)
            continue
        #look up in the dataframe
        if int(polarization*100) == 100 or int(polarization*100) == 0:
            #this can't be looked up in the table but it's the same as getting zero
            blue_states = 0
        else:
            blue_states = blue_df.loc[degree, str(int(polarization * 100))]
        if blue_states == 0:
            vals.append(0)
        else:
            vals.append(1.0/blue_states)
    if sum(vals) == 0:
        print("Error models.py deterministic_model(): the deterministic model doesn't work if you can't win any battlefields")
        quit()
    fractions = [val/sum(vals) for val in vals]
    #apportion the resources based on these fractions
    allocations = []
    for frac in fractions:
        allocations.append(math.floor(frac*RESOURCES))
    return allocations


def predictive_model(features):
    deterministic_allocations = deterministic_model(features)
    #select n/2 + 1 lowest allocated battlefields
    num_bf = int(NUM_BATTLEFIELDS/2 + 1)
    indices = sorted(range(len(deterministic_allocations)), key=lambda sub: deterministic_allocations[sub])[:int(num_bf)]
    det_selected_allocations = []
    for i in indices:
        det_selected_allocations.append(deterministic_allocations[i])
    pred_selected_allocations = [0]*num_bf
    gap = (RESOURCES-sum(det_selected_allocations))/num_bf
    for i in range(num_bf):
        pred_selected_allocations[i] = det_selected_allocations[i] + gap
    all_allocations = [0]*NUM_BATTLEFIELDS
    j = 0
    for i in indices:
        all_allocations[i] = pred_selected_allocations[j]
        j += 1
    return all_allocations


def reactive_model(features):
    deterministic_allocations = deterministic_model(features)
    #select n/2 + 1 lowest allocated battlefields
    num_bf = int(NUM_BATTLEFIELDS/2 + 1)
    print(num_bf)
    indices = sorted(range(len(deterministic_allocations)), key=lambda sub: deterministic_allocations[sub])[-int(num_bf):]
    print(indices)
    det_selected_allocations = []
    for i in indices:
        det_selected_allocations.append(deterministic_allocations[i])
    pred_selected_allocations = [0]*num_bf
    gap = (RESOURCES-sum(det_selected_allocations))/num_bf
    for i in range(num_bf):
        pred_selected_allocations[i] = det_selected_allocations[i] + gap
    all_allocations = [0]*NUM_BATTLEFIELDS
    j = 0
    for i in indices:
        all_allocations[i] = pred_selected_allocations[j]
        j += 1
    return all_allocations

def run(p1_model, p2_model):
    #Set up the battlefields
    battlefields = []
    color = 0 #this tells us that POLARIZATION = % that are blue, which is also true for our heatmaps
    features = [] #this should be a list of [polarization, avg_degree] for every battlefield, updated after every round
    for i in range(0, NUM_BATTLEFIELDS):
        battlefields.append(create_nodes())
        color_nodes(battlefields[i], color)
        color = not color
        if color == 0: #if blue
            features.append([POLARIZATION, WATTS_STROGATZ_K])
        else:
            features.append([1-POLARIZATION, WATTS_STROGATZ_K])

    print("STARTING NETWORK")
    for i in battlefields:
        print(i)

    converged = False
    num_rounds = 0
    while not converged:
        num_rounds += 1
        print("ROUND " + str(num_rounds))
        #pick initial guesses to enter in user_input
        p1_nums=None; p2_nums=None #this way if you don't set it to either random or deterministic you get user input
        if p1_model == "D":
            p1_nums = deterministic_model(features)
        elif p1_model == "R":
            p1_nums = random_model(features)
        elif p1_model == "P":
            p1_nums = predictive_model(features)
        elif p1_model == "A":
            p1_nums = reactive_model(features)

        if p2_model == "D":
            p2_nums = deterministic_model(features)
        elif p2_model == "R":
            p2_nums = random_model(features)
        elif p2_model == "P":
            p2_nums = predictive_model(features)
        elif p2_model == "A":
            p2_nums = reactive_model(features)

        #run the game with initial guesses
        polarizations = run_game(battlefields, THRESHOLD, player1_vals=p1_nums, player2_vals=p2_nums)
        for i in range(len(polarizations)):
            features[i][0] = polarizations[i]

        #check for convergence
        #need to check if ALL battlefields have converged...
        converged = True
        for p in polarizations:
            if p != 0.0 and p != 1.0:
                converged = False
        if num_rounds >= 15:
            print("Failed to converge in 15 rounds")
            converged=True

run("D", "A")
# #D for deterministic model and R for random model
