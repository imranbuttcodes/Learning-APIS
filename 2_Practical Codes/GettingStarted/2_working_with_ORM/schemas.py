from datetime import datetime

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

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


class UserOut(BaseModel):
    id: int
    email: str

    model_config = {
        "from_attributes": True
    }




# RESPONSE SCHEMAS

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut

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

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    # Enforce that 'dir' must be exactly 0 or 1
    dir: int = Field(ge=0, le=1)

class PostOut(BaseModel):
# 'Post' must exactly match the model name queried in SQLAlchemy
    Post: PostResponse
    votes: int

    model_config = {
        "from_attributes": True
    }