import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np # For creating sample data
import pandas

# read in data from file
#need to read in as arrays
red_df = pandas.read_csv('blotter_ai/data/red_data.csv')
blue_df = pandas.read_csv('blotter_ai/data/blue_data.csv')

red_df = red_df.drop(columns=red_df.columns[0], axis=1)

#kind of a janky way of getting them both into the same plot: just set blue wins to negative numbers
#won't work in the long run bc the AI can't work with negative states, but I just want to see it.
blue_df = blue_df.drop(columns=blue_df.columns[0], axis=1)
new_df = red_df.subtract(blue_df)
new_df = new_df.mask(new_df == 0, np.nan)

plt.figure(figsize=(8, 6)) # Optional: Adjust figure size
cmap = sns.color_palette("vlag", as_cmap=True)
cmap.set_bad('black')
sns.heatmap(new_df, cmap=cmap, annot=True, fmt=".2f")
annot=True # displays the values in each cell
fmt=".2f" # formats the annotations to two decimal places

"""
https://seaborn.pydata.org/generated/seaborn.heatmap.html
"""

plt.title('Heatmap')
plt.xlabel('Polarization')
plt.ylabel('Average Degree')


plt.show()