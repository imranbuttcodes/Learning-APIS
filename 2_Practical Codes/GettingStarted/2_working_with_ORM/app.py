from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session 
from dotenv import load_dotenv

# Database imports
from .databases import Base, engine, SessionLocal
from .models import Post

load_dotenv()

app = FastAPI()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- PYDANTIC MODELS (Data Validation) ---
# Renamed to PostCreate to avoid clashing with the SQLAlchemy Post model
class PostCreate(BaseModel):
   title: str = Field(..., example="My First Post")
   content: str = Field(..., example="This is the content of my first post.")
   published: bool = Field(default=True, example=True)
   # Removed the manual 'id' generation since Postgres/SQLAlchemy will handle IDs automatically!

# --- ROUTES ---

@app.get("/")
def root():
    return {"Hello": "This is Imran Butt Learning FastAPI"}

@app.get("/sqlalchemy_test")
def test_sqlalchemy(db: Session = Depends(get_db)):
    return {"message": "SQLAlchemy is working!", "db_url": str(engine.url)}

# 1. CREATE A POST
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # Unpack the Pydantic model directly into the SQLAlchemy model
    new_post = Post(**post.model_dump())
    
    db.add(new_post) # Add to the session
    db.commit()      # Commit to the database
    db.refresh(new_post) # Retrieve the new post (with its newly created ID)
    
    return {"data": new_post} 

# 2. GET ALL POSTS
@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
    # Equivalent to "SELECT * FROM posts"
    posts = db.query(Post).all()
    return {"data": posts}

# 3. GET A SPECIFIC POST
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # Equivalent to "SELECT * FROM posts WHERE id = {id}"
    post = db.query(Post).filter(Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"data": post}

# 4. UPDATE A POST
@app.put("/posts/{id}")
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    # Update the dictionary of values
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    
    return {"data": post_query.first()}  

# 5. DELETE A POST
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)