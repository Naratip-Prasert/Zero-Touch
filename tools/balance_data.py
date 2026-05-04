import pandas as pd

df = pd.read_csv("data/gesture_data.csv", header=None)

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

min_count = y.value_counts().min()

balanced_df = []

for label in y.unique():
    subset = df[y == label].sample(min_count)
    balanced_df.append(subset)

balanced_df = pd.concat(balanced_df)

balanced_df = balanced_df.sample(frac=1).reset_index(drop=True)

balanced_df.to_csv("data/gesture_data_balanced.csv", index=False, header=False)

print("Balanced done")