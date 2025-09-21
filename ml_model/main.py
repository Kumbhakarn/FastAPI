"""
Main FastAPI Application for Machine Learning Predictions.

This file serves as the entry point for the ML prediction API.
It exposes REST endpoints to interact with a trained ML model,
supporting both single predictions and batch predictions.

Author: [Your Name]
"""

from fastapi import FastAPI
from ml_model.schemas import InputSchema, OutputSchema  # Pydantic schemas for request/response validation
from ml_model.predict import make_predictions, make_batch_predictions  # Functions that interact with ML model
from typing import List

# Initialize FastAPI application
app = FastAPI(
    title="ML Model Prediction API",
    description="This API provides endpoints for single and batch predictions using a trained ML model.",
    version="1.0.0"
)

# Root endpoint to check if API is running
@app.get('/')
def index():
    return {'message': 'Welcome to the ML model prediction API'}

# -------------------------------------------------------------------------
# Endpoint: Single Prediction
# Accepts a single input payload and returns one prediction result.
# -------------------------------------------------------------------------
@app.post('/prediction', response_model=OutputSchema)
def predict(user_input: InputSchema):
    # Convert validated Pydantic object into dictionary
    prediction = make_predictions(user_input.model_dump())  
    # Return prediction rounded to 2 decimal places
    return OutputSchema(predicted_price=round(prediction, 2))


# -------------------------------------------------------------------------
# Endpoint: Batch Predictions
# Accepts a list of inputs and returns a list of prediction results.
# Useful for vectorized or bulk inference.
# -------------------------------------------------------------------------
@app.post('/batch_prediction', response_model=List[OutputSchema])
def batch_predict(user_inputs: List[InputSchema]):
    # Convert list of Pydantic objects to list of dictionaries
    predictions = make_batch_predictions([x.model_dump() for x in user_inputs])
    # Return each prediction rounded to 2 decimal places
    return [OutputSchema(predicted_price=round(prediction, 2)) for prediction in predictions]
