from fastapi import FastAPI
from pydantic import BaseModel


# Pydantic BaseModel
class User(BaseModel):
    id: int
    name: str


# Assign Object to Class FastAPI
app = FastAPI()

# Endpoint 
@app.get('/user', response_model=User)
def get_user():
    return User(id=1,name='Bruce')