from unittest.mock import patch
import numpy as np
from mock_ml.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_predict_with_mock():
    # patch where it's USED (mock_ml.main.log_model)
    with patch('mock_ml.main.log_model.predict') as mock_predict:
        mock_predict.return_value = [99]

        response = client.post(
            "/predict",
            json={
                "SepalLengthCm": 5.2,
                "SepalWidthCm": 3.5,
                "PetalLengthCm": 1.5,
                "PetalWidthCm": 0.2
            }
        )

        assert response.status_code == 200
        assert response.json() == {'prediction': 99}

        # Extract the arguments passed to mock_predict
        args, kwargs = mock_predict.call_args

        expected = np.array([[5.2, 3.5, 1.5, 0.2]])
        np.testing.assert_array_equal(args[0], expected)