import os
import joblib
import pandas as pd

from feature_extractor import extract_features
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

DATASET_FOLDER = "dataset/samples"

model = joblib.load("trained_model.pkl")

results = []

print("Starting model evaluation...")
print("Dataset folder:", DATASET_FOLDER)

for filename in os.listdir(DATASET_FOLDER):

    if filename.endswith(".py"):

        filepath = os.path.join(DATASET_FOLDER, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            code = file.read()

        features = extract_features(code)

        X = pd.DataFrame([features])

        prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0]
        confidence = round(max(probability) * 100, 2)

        if filename.startswith("buggy"):
            actual_label = 1
            actual_text = "Buggy"
        else:
            actual_label = 0
            actual_text = "Not Buggy"

        predicted_text = "Buggy" if prediction == 1 else "Not Buggy"

        correct = actual_label == prediction

        results.append({
            "filename": filename,
            "actual": actual_text,
            "predicted": predicted_text,
            "confidence": confidence,
            "correct": correct,
            "loops": features["loops"],
            "functions": features["functions"],
            "ifs": features["ifs"],
            "imports": features["imports"],
            "try_blocks": features["try_blocks"],
            "lines": features["lines"],
            "syntax_error": features["syntax_error"]
        })

df = pd.DataFrame(results)

df.to_csv("dataset/evaluation_results.csv", index=False)

y_true = [1 if row["actual"] == "Buggy" else 0 for _, row in df.iterrows()]
y_pred = [1 if row["predicted"] == "Buggy" else 0 for _, row in df.iterrows()]

accuracy = accuracy_score(y_true, y_pred)
matrix = confusion_matrix(y_true, y_pred)
report = classification_report(y_true, y_pred)

print("\nEvaluation Results:")
print(df)

print("\nAccuracy:", round(accuracy * 100, 2), "%")

print("\nConfusion Matrix:")
print(matrix)

print("\nClassification Report:")
print(report)

print("\nResults saved to dataset/evaluation_results.csv")