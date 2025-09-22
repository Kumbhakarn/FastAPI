import joblib
import os

# Build the correct path to the joblib file inside mock_ml
model_path = os.path.join(os.path.dirname(__file__), "log_model.joblib")

log_model = joblib.load(model_path)
