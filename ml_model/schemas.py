"""
schemas.py — Core data models for the FastAPI ML Prediction API.

This is typically the FIRST file you create when building a FastAPI project
for a machine learning application. Schemas act as the foundation of the API,
defining the structure and validation of both incoming requests (features for
prediction) and outgoing responses (predicted results).

Why start here?
---------------
- Clearly defines what data the ML model expects.
- Ensures strict validation of input before hitting the model.
- Provides a contract between the backend and the client (request/response shape).
- Makes API development faster and safer.

Example Input (JSON):
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

Example Output (JSON):
{
    "predicted_price": 452100.75
}


"""

from pydantic import BaseModel, StrictInt, Field

# -------------------------------------------------------------------------
# Input Schema
# Defines the structure and validation rules for the features
# that will be passed to the ML model for prediction.
# -------------------------------------------------------------------------
class InputSchema(BaseModel):
    """
    Schema for model input features.

    Attributes:
        longitude (float): Longitude of the location.
        latitude (float): Latitude of the location.
        housing_median_age (int): Median age of the houses (must be > 0).
        total_rooms (int): Total number of rooms in the block (must be > 0).
        total_bedrooms (int): Total number of bedrooms in the block (must be > 0).
        population (int): Population of the block (must be > 0).
        households (int): Number of households in the block (must be > 0).
        median_income (float): Median income of households (must be > 0).
    """
    longitude: float
    latitude: float
    housing_median_age: int = Field(..., gt=0)
    total_rooms: StrictInt = Field(..., gt=0)
    total_bedrooms: StrictInt = Field(..., gt=0)
    population: int = Field(..., gt=0)
    households: StrictInt = Field(..., gt=0)
    median_income: float = Field(..., gt=0)


# -------------------------------------------------------------------------
# Output Schema
# Defines the structure of the response returned by the ML model prediction.
# -------------------------------------------------------------------------
class OutputSchema(BaseModel):
    """
    Schema for model prediction output.

    Attributes:
        predicted_price (float): The predicted house price.
    """
    predicted_price: float
