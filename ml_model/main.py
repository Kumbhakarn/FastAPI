from fastapi import FastAPI
from ml_model.schemas import InputSchema, OutputSchema
from ml_model.predict import make_predictions,make_batch_predictions
from typing import List

app = FastAPI()

@app.get('/')
def index():
    return {'message':'Welcome to the ML model prediction API'}

# This end-point is for single prediction

@app.post('/prediction', response_model=OutputSchema)
def predict(user_input: InputSchema):
    prediction = make_predictions(user_input.model_dump())# implicitly convert json object to python dictionary
    return OutputSchema(predicted_price=round(prediction, 2))


# This end-point is for Batch predictions (Vectorized Batch) multiple input multiple output
@app.post('/batch_prediction', response_model=List[OutputSchema])
def batch_predict(user_inputs: List[InputSchema]):
    predictions = make_batch_predictions([x.model_dump() for x in user_inputs])
    return [OutputSchema(predicted_price=round(prediction, 2)) for prediction in predictions]