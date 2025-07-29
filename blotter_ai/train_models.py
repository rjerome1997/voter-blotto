import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import joblib

""""NOTE: red = 1, blue = 0"""

red_df = pd.read_csv('data/red_data.csv')
blue_df = pd.read_csv('data/blue_data.csv')
red_df = red_df.drop(columns=red_df.columns[0], axis=1)
blue_df = blue_df.drop(columns=blue_df.columns[0], axis=1)

"""
COMBINE RED AND BLUE DATA INTO A PREPROCESSED DATAFRAME
"""
d = {'polarization':[], 'avg_degree':[], 'num_states': [], 'color':[]}
#ITERATE OVER COLUMNS ONE BY ONE
for column_name, column in red_df.items():
    degree = 5
    for val in column:
        if val != 0:
            d['polarization'].append(int(column_name))
            d['num_states'].append(val)
            d['color'].append(1)
            d['avg_degree'].append(degree)
        degree += 1

for column_name, column in blue_df.items():
    degree = 5
    for val in column:
        if val != 0:
            d['polarization'].append(int(column_name))
            d['num_states'].append(val)
            d['color'].append(0)
            d['avg_degree'].append(degree)
        degree += 1
combined_df = pd.DataFrame(d)

combined_df.to_csv("data/combined_data.csv")

"""THIS IS WHERE WE PUT IN THE FEATURES: THE INITIAL STATE OF THE NETWORK"""
"""
* So I believe we need to specify column names from the CSV and these are the "features" or the qualities it will consider
* So in this case I guess the percentages? But we also need to take polarization into account... 
"""
features = ['polarization', 'avg_degree']
X = combined_df[features]

"""NOW WE NEED TO ESTABLISH TARGETS: WE WANT TO KNOW WHAT COLOR IT CONVERGED TO AND HOW LONG IT TOOK"""
"""
* So y_outcome needs to be a list of all combinations and what color they converged to
* and y_time needs to be a list of all combinations and how long they took to converge
"""

y_outcome = combined_df['color']
y_time = combined_df['num_states']

"""AND NOW WE TRAIN THE MODELS."""
"""
* We need to combine red and blue data because we need just ONE X, not a red one and a blue one
"""

clf = RandomForestClassifier(n_estimators=100, max_features=2)
clf.fit(X.values, y_outcome.values)

reg = RandomForestRegressor()
reg.fit(X.values, y_time.values)

print(clf.score(X.values, y_outcome.values))
X_test_dict = {"polarization": [0.01], "avg_degree":[100]}
X_test_df = pd.DataFrame(X_test_dict)
print(clf.predict_proba(X_test_df.values))

"""NOW WE SAVE THE MODELS TO USE AGAIN LATER"""

joblib.dump(clf, 'models/outcome_model.pkl')
joblib.dump(reg, 'models/time_model.pkl')
