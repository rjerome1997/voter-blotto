import math
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import json
import numpy as np
from joblib import delayed


def get_range(data, feature):
    min = 10000000; max = 0
    for graph_dict in data:
        if graph_dict[feature] < min:
            min = graph_dict[feature]
        if graph_dict[feature] > max:
            max = graph_dict[feature]
    r = max - min

    print(feature)
    print("r", r, "max", max, "min", min)

    return r

def buckets(num_buckets, data, feature1, feature2):
    r1 = get_range(data, feature1)
    width1 = r1/num_buckets
    print("width", width1)
    new_data = []
    for graph_dict in data:
        index = graph_dict[feature1]//width1
        d = {}
        d[feature2] = graph_dict[feature2]
        d['num_rounds'] = graph_dict['num_rounds']
        #d['index'] = index
        d['bucket_name'] = round(index*width1, 2)
        new_data.append(d)
    df = pd.DataFrame(new_data)
    df = df.groupby([feature2, 'bucket_name']).mean()
    # for element in bucketed df
    rows = []; cols = []
    for i, row in df.iterrows():
        if i[0] not in rows:
            rows.append(i[0])
        if i[1] not in cols:
            cols.append(i[1])
    # create a display_df that has these lists as its parameters and is full of dummy data that is just zeroe
    dummy_data = np.zeros((len(rows), len(cols)))
    display_df = pd.DataFrame(dummy_data, index=rows, columns=cols.sort())
    # for element in bucketed df
    for i, row in df.iterrows():
        display_df.at[i[0], i[1]] = row['num_rounds']

    # Now repeat the process and average the rows instead of the columns
    r2 = get_range(data, feature2)
    width2 = r2 / num_buckets

    display_df[feature2] = (display_df.index//width2)*width2
    display_df[feature2] = round(display_df[feature2], 2)

    display_df = display_df.groupby(feature2).mean()
    display_df = display_df.sort_values(by=feature2, ascending=False)

    #remove columns with no valid data
    for col in display_df:
        if (display_df[col] == 0).all():
            display_df = display_df.drop(col, axis=1)
        elif (display_df[col] == 100).all():
            display_df = display_df.drop(col, axis=1)

    #display_df = display_df.iloc[:, :-15]

    return display_df


# read in data from file
#need to read in as arrays
with open("C:\\Users\\renee\\PycharmProjects\\blotter\\blotter_ai\\data\\data_300_nodes.json", 'r') as f:
    data = json.load(f)

#okay, we need to convert it into some kind of 2D array
#currently a list of dictionaries
#df = pd.DataFrame(data)

#process data by putting num_maximal_blue_nodes into buckets

"""for i in range(0,10):
    graph = data[i]
    row_names.append(graph['polarization'])
    col_names.append(graph['num_maximal_blue_nodes'])
reduced_df = pd.DataFrame(dummy_data, index=row_names, columns=col_names)
for i in range(0,10):
    graph = data[i]
    reduced_df.at[graph['polarization'], graph['num_maximal_blue_nodes']] = graph['num_rounds']"""


x_feature = 'p'
y_feature = 'polarization'

bucketed_df = buckets(40, data, x_feature, y_feature)
bucketed_df = bucketed_df.mask(bucketed_df == 0, np.nan)
bucketed_df = bucketed_df.astype(str)
bucketed_df = bucketed_df.mask(bucketed_df == "100", ">100")

#plt.figure(figsize=(8, 6)) # Optional: Adjust figure size
cmap = sns.color_palette("crest", as_cmap=True)
cmap.set_bad('black')
sns.heatmap(bucketed_df, cmap=cmap, annot=True, fmt=".2f")

plt.title(str(x_feature) + " vs " + str(y_feature))

plt.show()