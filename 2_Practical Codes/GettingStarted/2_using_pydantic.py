from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class User(BaseModel):
    name: str = Field(..., example="John Doe")   # here ... means this field is required
    age: int = Field(
        gt=0,
        lt = 150,
        description="User's age"
    )
    is_new: bool = Field(default=True, example=True)
    gender: Optional[str] = Field(default=None, example="Male")


@app.get("/")
def read_root():
    return {"Hello": "This is Imran Butt Learning FastAPI"}


@app.post("/users")
def create_user(user: User):
    print("Creating a user...")
    print("User Data: ", user)
    print(user.name)
    print(type(user.model_dump()))
    return user.model_dump()  # return the user data as a dictionary