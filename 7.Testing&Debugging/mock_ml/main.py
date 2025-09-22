from fastapi import FastAPI
from pydantic import BaseModel
from mock_ml.model import log_model
import numpy as np


app = FastAPI()


class IrisFlower(BaseModel):
    SepalLengthCm: float
    SepalWidthCm: float
    PetalLengthCm: float
    PetalWidthCm: float


# Endpoints
@app.post('/predict')
def predict(data: IrisFlower):
    features = np.array([
        [
            data.SepalLengthCm,
            data.SepalWidthCm,
            data.PetalLengthCm,
            data.PetalWidthCm
        ]
    ])
    prediction = log_model.predict(features)
    return {'prediction':int(prediction[0])}