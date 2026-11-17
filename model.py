import pandas as pd
import pickle

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# Load Excel dataset
df = pd.read_excel(
    "Campus_Waste_Watch.xlsx",
    sheet_name="Observations"
)

print("Dataset loaded successfully!")

# Required columns
required_columns = [
    "Date",
    "Time",
    "Location",
    "Fill_Level_Percent",
    "Hours_Since_Collection",
    "Waste_Type",
    "Event_Day",
    "Overflow_Before_Next_Collection"
]

# Check missing columns
missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )

# Prepare dataset
df["DateTime"] = pd.to_datetime(
    df["Date"].astype(str) + " " + df["Time"].astype(str),
    errors="coerce"
)

df = df.dropna(subset=["DateTime"])

df = df.sort_values("DateTime")

# Features
features = [
    "Location",
    "Fill_Level_Percent",
    "Hours_Since_Collection",
    "Waste_Type",
    "Event_Day"
]

X = df[features]

y = pd.to_numeric(
    df["Overflow_Before_Next_Collection"],
    errors="coerce"
)

# Remove invalid target rows
valid_rows = y.isin([0, 1])

X = X.loc[valid_rows]
y = y.loc[valid_rows].astype(int)

if y.nunique() < 2:
    raise ValueError(
        "The dataset must contain both overflow classes: 0 and 1."
    )

# Split data chronologically
unique_dates = sorted(df.loc[valid_rows, "DateTime"].dt.date.unique())

if len(unique_dates) < 2:
    raise ValueError(
        "At least two different dates are required for a time-based split."
    )

split_position = max(1, int(len(unique_dates) * 0.8))

train_dates = unique_dates[:split_position]
test_dates = unique_dates[split_position:]

train_mask = df.loc[valid_rows, "DateTime"].dt.date.isin(train_dates)
test_mask = df.loc[valid_rows, "DateTime"].dt.date.isin(test_dates)

X_train = X.loc[train_mask]
X_test = X.loc[test_mask]

y_train = y.loc[train_mask]
y_test = y.loc[test_mask]

if (
    X_train.empty
    or X_test.empty
    or y_train.nunique() < 2
    or y_test.nunique() < 2
):
    raise ValueError(
        "Training and testing data must both contain records "
        "from both overflow classes. Collect more varied observations."
    )

# Preprocessing
categorical_columns = [
    "Location",
    "Waste_Type"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_columns
        )
    ],
    remainder="passthrough"
)

# Machine learning model
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                class_weight="balanced"
            )
        )
    ]
)

# Train model
model.fit(X_train, y_train)

print("Model trained successfully!")

# Evaluate model
predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("Test Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

# Save model
with open("waste_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("\nModel saved successfully!")
