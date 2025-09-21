"""
train.py — Training script for the ML Prediction API.

Purpose:
--------
This file is responsible for:
1. Loading and preprocessing the dataset.
2. Training a machine learning model (Linear Regression in this case).
3. Serializing and saving the trained model as a `.joblib` file for later use
   in prediction (via `predict.py` and FastAPI endpoints).

Why important?
--------------
- This script is usually run only once (or occasionally to retrain).
- The saved model (`model.joblib`) is then loaded by the API for inference.
- Keeps training logic separate from API code.

"""

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

# -------------------------------------------------------------------------
# Step 1: Load dataset
# Provide the dataset file path. Replace with your dataset location.
# -------------------------------------------------------------------------
file_path = r"D:\16_FastAPI\housing.csv"

# Read CSV, drop null values, and ignore the last column (if not needed)
df = pd.read_csv(file_path).iloc[:, :-1].dropna()
print("✅ Dataset loaded successfully")

# -------------------------------------------------------------------------
# Step 2: Split dataset into features (X) and target (y)
# -------------------------------------------------------------------------
X = df.drop(columns="median_house_value")  # Features
y = df["median_house_value"].copy()        # Target variable
print("✅ Dataset split into features and target")

# -------------------------------------------------------------------------
# Step 3: Train the model
# Using Linear Regression for this example
# -------------------------------------------------------------------------
model = LinearRegression().fit(X, y)
print("✅ Model trained successfully")

# -------------------------------------------------------------------------
# Step 4: Serialize (save) the trained model
# This file will later be used by `predict.py` for inference.
# -------------------------------------------------------------------------
joblib.dump(model, "model.joblib")
print("✅ Model saved as 'model.joblib'")
