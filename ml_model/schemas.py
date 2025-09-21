# for the api we are passing the data here 
from pydantic import BaseModel, StrictInt, Field


## This class is import schema for ML model 
## so we are defining the features of the dataset that will feed to predict the ml model
class InputSchema(BaseModel):
    longitude: float
    latitude: float
    housing_median_age: int = Field(..., gt = 0)
    total_rooms: StrictInt = Field(..., gt = 0)
    total_bedrooms: StrictInt = Field(..., gt = 0)
    population: int = Field(..., gt = 0)
    households: StrictInt = Field(..., gt = 0)
    median_income: float = Field(..., gt = 0)



### Output Schema

class OutputSchema(BaseModel):
    predicted_price: float
