from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session 
from dotenv import load_dotenv
from .utils import hash_password
from .databases import Base, engine, get_db
from .models import Post, User
from .schemas import PostCreate, PostResponse, UserCreate, UserResponse
from .routers import user,post


load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

# --- ROUTES ---



app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"Hello": "This is Imran Butt Learning FastAPI"}
