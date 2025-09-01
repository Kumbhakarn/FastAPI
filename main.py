from fastapi import FastAPI

# Initialize the object for Class FastAPi
app = FastAPI()

# Endpoints to routes of our app
@app.get('/')
def index():
    return {'message':'Hello, FashtAPI!'}



