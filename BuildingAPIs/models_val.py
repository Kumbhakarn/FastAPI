from pydantic import BaseModel, Field, StrictInt
from typing import Optional

class Employee(BaseModel):
    id: int = Field(...,gt=0) ## required Field (...) for greater than gt=0
    name: str = Field(..., min_length=3,max_length=30)
    department: str = Field(..., min_length=3,max_length=30)
    age: int = Field(..., gt=18, description='Age must be greater than 18')
    # age: Optional[int] = Field(default=None) Optional Field can be included like this
    # age: Optional[StrictInt] = Field(default=None) # -> Strictly checks the value is entered is integer or not
    # like wise we have -> , StrictBool, StrictBytes, StrictFloat, SecretStr
