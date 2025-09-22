"""
main.py — FastAPI Application for ML Model Predictions

Purpose:
--------
This is the ENTRY POINT of the FastAPI ML project.
It wires together:
- Input/Output schemas (from schemas.py)
- Prediction functions (from predict.py)
- REST endpoints for single and batch predictions

Endpoints:
----------
1. GET    /                   → Health check / welcome message
2. POST   /prediction         → Single prediction
3. POST   /batch_prediction   → Batch predictions (vectorized)

How to run:
-----------
    uvicorn main:app --reload

Example Single Request (JSON):
{
    "longitude": -122.23,
    "latitude": 37.88,
    "housing_median_age": 41,
    "total_rooms": 880,
    "total_bedrooms": 129,
    "population": 322,
    "households": 126,
    "median_income": 8.3252
}

Example Single Response (JSON):
{
    "predicted_price": 452100.75
}

"""

from fastapi import FastAPI
from ml_model.schemas import InputSchema, OutputSchema  # Request/response validation
from ml_model.predict import make_predictions, make_batch_predictions  # ML model inference functions
from typing import List

# -------------------------------------------------------------------------
# Initialize FastAPI application
# -------------------------------------------------------------------------
app = FastAPI(
    title="ML Model Prediction API",
    description="This API provides endpoints for single and batch predictions using a trained ML model.",
    version="1.0.0"
)

# -------------------------------------------------------------------------
# Root Endpoint (Health Check)
# -------------------------------------------------------------------------
@app.get("/")
def index():
    """
    Root endpoint to confirm API is running.

    Returns:
        dict: A simple welcome message.
    """
    return {"message": "Welcome to the ML model prediction API"}


# -------------------------------------------------------------------------
# Endpoint: Single Prediction
# -------------------------------------------------------------------------
@app.post("/prediction", response_model=OutputSchema)
def predict(user_input: InputSchema):
    """
    Generate a single prediction from one input payload.

    Args:
        user_input (InputSchema): Validated input data.

    Returns:
        OutputSchema: Predicted house price (rounded to 2 decimals).
    """
    # Convert validated Pydantic object into a dictionary
    prediction = make_predictions(user_input.model_dump())

    # Return prediction wrapped in OutputSchema
    return OutputSchema(predicted_price=round(prediction, 2))


# -------------------------------------------------------------------------
# Endpoint: Batch Predictions
# -------------------------------------------------------------------------
@app.post("/batch_prediction", response_model=List[OutputSchema])
def batch_predict(user_inputs: List[InputSchema]):
    """
    Generate predictions for multiple input payloads at once.

    Args:
        user_inputs (List[InputSchema]): List of validated input data.

    Returns:
        List[OutputSchema]: List of predicted house prices (rounded to 2 decimals).
    """
    # Convert list of Pydantic objects to list of dictionaries
    predictions = make_batch_predictions([x.model_dump() for x in user_inputs])

    # Wrap predictions in OutputSchema objects
    return [OutputSchema(predicted_price=round(prediction, 2)) for prediction in predictions]
