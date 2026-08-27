from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


# REQUEST SCHEMAS

class PostCreate(BaseModel):
    title: str = Field(
        ...,
        example="My First Post"
    )

    content: str = Field(
        ...,
        example="This is the content of my first post."
    )

    published: bool = Field(
        default=True,
        example=True
    )


# RESPONSE SCHEMAS

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class UserCreate(BaseModel):
    email: EmailStr
    password: str   


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = {
        "from_attributes": True
    }


class UserLogin(BaseModel):
    email: EmailStr
    password: str