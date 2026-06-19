import os
import subprocess
import pandas as pd

DATASET_FOLDER = "dataset/samples"

results = []

print("Starting Pylint baseline test...")
print("Checking folder:", DATASET_FOLDER)

files = os.listdir(DATASET_FOLDER)

print("Files found:", len(files))

for filename in files:

    if filename.endswith(".py"):

        print("Checking:", filename)

        filepath = os.path.join(DATASET_FOLDER, filename)

        if filename.startswith("buggy"):
            actual_label = "Buggy"
        else:
            actual_label = "Not Buggy"

        try:
            result = subprocess.run(
                ["pylint", filepath, "--score=n"],
                capture_output=True,
                text=True
            )

            output = result.stdout + result.stderr

            if (
                "undefined-variable" in output.lower()
                or "syntax-error" in output.lower()
                or "used-before-assignment" in output.lower()
                or "division-by-zero" in output.lower()
                or "undefined-loop-variable" in output.lower()
                or result.returncode != 0
            ):
                pylint_prediction = "Buggy"
            else:
                pylint_prediction = "Not Buggy"

        except Exception as e:
            pylint_prediction = "Error Running Pylint"
            print("Error:", e)

        correct = actual_label == pylint_prediction

        results.append({
            "filename": filename,
            "actual_label": actual_label,
            "pylint_prediction": pylint_prediction,
            "correct": correct
        })

df = pd.DataFrame(results)

print("\nPylint Results:")
print(df)

df.to_csv("dataset/pylint_baseline_results.csv", index=False)

if len(df) > 0:
    accuracy = df["correct"].mean() * 100
    print("\nPylint Baseline Accuracy:", round(accuracy, 2), "%")
else:
    print("\nNo Python files were processed.")

print("\nResults saved to dataset/pylint_baseline_results.csv")