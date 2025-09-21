"""
predict.py — Inference utilities for the ML Prediction API.

Purpose:
--------
This file is responsible for:
1. Loading the serialized (trained) ML model from `model.joblib`.
2. Defining utility functions to generate predictions:
   - Single prediction (for one input record).
   - Batch prediction (for multiple input records at once).

Why important?
--------------
- Keeps prediction logic separate from training (`train.py`) and API (`main.py`).
- Provides reusable functions (`make_predictions`, `make_batch_predictions`)
  that can be imported by the FastAPI app or other scripts.

Author: [Your Name]
"""

import joblib
import numpy as np
from typing import List

# -------------------------------------------------------------------------
# Step 1: Load the trained ML model from disk
# -------------------------------------------------------------------------
saved_model = joblib.load("model.joblib")
print("✅ Loaded the trained model from 'model.joblib'")


# -------------------------------------------------------------------------
# Step 2: Define function for single prediction
# -------------------------------------------------------------------------
def make_predictions(data: dict) -> float:
    """
    Generate prediction for a single input record.

    Args:
        data (dict): A dictionary containing the input features required
                     by the ML model.

    Returns:
        float: The predicted value (e.g., house price).
    """
    # Convert dictionary to a 2D NumPy array (1 row, n features)
    features = np.array([[
        data["longitude"],
        data["latitude"],
        data["housing_median_age"],
        data["total_rooms"],
        data["total_bedrooms"],
        data["population"],
        data["households"],
        data["median_income"]
    ]])

    # Return the first (and only) prediction
    return saved_model.predict(features)[0]


# -------------------------------------------------------------------------
# Step 3: Define function for batch prediction
# -------------------------------------------------------------------------
def make_batch_predictions(data: List[dict]) -> np.ndarray:
    """
    Generate predictions for multiple input records at once.

    Args:
        data (List[dict]): A list of dictionaries, where each dictionary
                           contains the input features required by the ML model.

    Returns:
        np.ndarray: A NumPy array containing predictions for each record.
    """
    # Convert list of dictionaries to a 2D NumPy array (m rows, n features)
    X = np.array([[
        x["longitude"],
        x["latitude"],
        x["housing_median_age"],
        x["total_rooms"],
        x["total_bedrooms"],
        x["population"],
        x["households"],
        x["median_income"]
    ] for x in data])

    # Return predictions for all rows
    return saved_model.predict(X)