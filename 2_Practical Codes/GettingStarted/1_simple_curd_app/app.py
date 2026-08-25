from fastapi import FastAPI, Response, status,HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import random # Import the module, not just randint
import psycopg2
from psycopg2.extras import RealDictCursor # Import RealDictCursor for better dictionary handling
app = FastAPI()
from dotenv import load_dotenv
import os

load_dotenv()




try:
    conn = psycopg2.connect(
        host = os.getenv('DB_HOST'), 
        port = os.getenv('DB_PORT'),
        database = os.getenv('DB_NAME'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD')
    )
    # RealDictCursor makes the output look like a Python dictionary instead of a tuple!
    cursor = conn.cursor(cursor_factory=RealDictCursor)  # we could also pass this as a parameter to the connect function, but this is more explicit
    print("Database connection was successful")
except Exception as e:
    print("Database connection failed")
    print("ERROR",e)

POSTS = [
    {
        'title': 'My First Post',
        'content': 'This is the content of my first post.',
        'published': True,
        'rating': 5,
        'id': 1
    },
    {
        'title': 'My Second Post',
        'content': 'This is the content of my second post.',
        'published': False,
        'rating': 4,
        'id': 2
    }
]

# Helper function to generate a random ID
def generate_id():
    return random.randint(1, 1000000)

class Post(BaseModel):
   title: str = Field(..., example="My First Post")
   content: str = Field(..., example="This is the content of my first post.")
   published: bool = Field(default=True, example=True)
   rating: Optional[int] = Field(default=None, gt=0, lt=6, example=5)
   
   # Use default_factory to run the function dynamically on every new request
   id: int = Field(default_factory=generate_id, example=1) 

@app.get("/")
def root():
    return {"Hello": "This is Imran Butt Learning FastAPI"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post_dict['title'], post_dict['content'], post_dict['published']))
    new_post = cursor.fetchone()
    conn.commit()  # Commit the transaction to save changes to the database
    # Return just the newly created post, not the whole list!
    return {"data": new_post} 

@app.get("/posts")
def get_all_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.get("/posts/latest")
def get_latest_post():
    if not POSTS:
        return None    
    return {"data": POSTS[-1]}


def find_post(id: int):
    for post in POSTS:
        if post["id"] == id:
            return post
    return None

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(detail=f"Post with id {id} not found", status_code=status.HTTP_404_NOT_FOUND)
    return {"data": post}


def find_post_index(id: int):
    for index, post in enumerate(POSTS):
        if post["id"] == id:
            return index
    return None

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()  # Commit the transaction to save changes to the database
    if deleted_post is None:
        raise HTTPException(detail=f"Post with id {id} not found", status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (updated_post.title, updated_post.content, updated_post.published, id))
    updated_post_data = cursor.fetchone()
    conn.commit()  # Commit the transaction to save changes to the database
    if updated_post_data is None:
        raise HTTPException(detail=f"Post with id {id} not found", status_code=status.HTTP_404_NOT_FOUND)
    return {"data": updated_post_data}  