from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session 
from dotenv import load_dotenv
from utils import hash_password
from databases import Base, engine, get_db
from models import Post, User
from schemas import PostCreate, PostResponse, UserCreate, UserResponse
from routers import user, post, auth, vote
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

app = FastAPI()

# Base.metadata.create_all(bind=engine)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


origins = [
    # # "http://localhost:3000", # Example React frontend
    # # "http://127.0.0.1:5500", # Example VS Code Live Server
    # "https://www.google.com"
    "*" # * means every origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"Hello": "This is Imran Butt Learning FastAPI"}
