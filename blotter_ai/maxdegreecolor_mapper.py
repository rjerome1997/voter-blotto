import math
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import json
import numpy as np
from joblib import delayed
from torch.cuda import graph

# read in data from file
#need to read in as arrays
with open("C:\\Users\\renee\\PycharmProjects\\blotter\\blotter_ai\\data\\data_300_nodes.json", 'r') as f:
    data = json.load(f)

#okay, we need to convert it into some kind of 2D array
#currently a list of dictionaries
#df = pd.DataFrame(data)

#process data by putting num_maximal_blue_nodes into buckets
num_blue_max = 0
num_red_max = 0
num_converge_blue = 0
num_converge_red = 0
for graph_dict in data:
    if graph_dict['red_in_top_ten'] > 5:
        num_red_max += 1
    if graph_dict['blue_in_top_ten'] > 5:
        num_blue_max += 1
    if 'color' in graph_dict:
        if graph_dict['color'] == 'blue':
            num_converge_blue += 1
        else:
            num_converge_red += 1

print("Blue:", num_converge_blue/num_blue_max)
print("Red:", num_converge_red/num_red_max)
