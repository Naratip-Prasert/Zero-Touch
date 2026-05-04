import pandas as pd

df = pd.read_csv("data/gesture_data.csv", header=None)

y = df.iloc[:, -1]

print(y.value_counts())