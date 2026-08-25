from fastapi import FastAPI, Response, status,HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import random # Import the module, not just randint

app = FastAPI()

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
    POSTS.append(post_dict)
    # Return just the newly created post, not the whole list!
    return {"data": post_dict} 

@app.get("/posts")
def get_all_posts():
    return {"data": POSTS}


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
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} not found."}
    return post


def find_post_index(id: int):
    for index, post in enumerate(POSTS):
        if post["id"] == id:
            return index
    return None

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_index = find_post_index(id)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found.")
    POSTS.pop(post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post):
    post_index = find_post_index(id)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found.")
    
    # Update the post while preserving the original ID
    POSTS[post_index] = updated_post.model_dump()
    POSTS[post_index]["id"] = id  # Ensure the ID remains unchanged
    return {"data": POSTS[post_index]}
