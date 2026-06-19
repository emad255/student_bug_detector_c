import os
import pandas as pd
from feature_extractor import extract_features

DATASET_FOLDER = "dataset/samples"

data = []

print("Scanning files...")

for filename in os.listdir(DATASET_FOLDER):

    print("Found:", filename)

    if filename.endswith(".py"):

        filepath = os.path.join(DATASET_FOLDER, filename)

        with open(filepath, "r") as f:
            code = f.read()

        features = extract_features(code)

        if filename.startswith("good"):
            label = 0
        else:
            label = 1

        features["filename"] = filename
        features["label"] = label

        data.append(features)

df = pd.DataFrame(data)

print(df)

df.to_csv("dataset/dataset.csv", index=False)

print("\nDataset created successfully.")