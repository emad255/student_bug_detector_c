import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load dataset
df = pd.read_csv("dataset/dataset.csv")

print("Dataset loaded:")
print(df)

# Features and label
X = df[
    [
        "loops",
        "functions",
        "ifs",
        "imports",
        "try_blocks",
        "lines",
        "syntax_error",
        "undefined_vars",
        "risky_ops",
        "has_bare_except"
    ]
]

y = df["label"]

# Split dataset (stratified to keep buggy/not-buggy ratio balanced)
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Test model
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

joblib.dump(model, "trained_model.pkl")

print("\nModel saved as trained_model.pkl")

importances = pd.Series(
    model.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

print("\nFeature importances:")
print(importances)