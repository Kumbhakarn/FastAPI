from fastapi import FastAPI

app = FastAPI()

# Decorator @app
@app.get('/') # / forward slash = HomePage {route/Endpoint} GET=retrieve : user is going to see the data
def home(): # root URL Function
    return {'message':'Hello FastAPI!'} # HomePage Message # Python Dict sent as json Object

