from ..models import Post, User, Vote
from ..schemas import PostCreate, PostResponse, TokenData, PostOut
from ..databases import get_db, engine
from fastapi import status, Depends, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session 
from ..oauth2 import get_current_user
from typing import Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/sqlalchemy_test")
def test_sqlalchemy(db: Session = Depends(get_db)):
    return {"message": "SQLAlchemy is working!", "db_url": str(engine.url)}

# 1. CREATE A POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db),current_user : User = Depends(get_current_user)):
    # Unpack the Pydantic model directly into the SQLAlchemy model
    print(f"The user creating this post has an ID of: {current_user.email}")
    
    new_post = Post(**post.model_dump(), owner_id = current_user.id)  
    
    db.add(new_post) # Add to the session
    db.commit()      # Commit to the database
    db.refresh(new_post) # Retrieve the new post (with its newly created ID)
    return new_post 

# About Query Parameters
# @router.get("/")
# def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0):
#     posts = db.query(Post).limit(limit).offset(skip).all()
#     print("Yoah")
#     return posts

# 2. GET ALL POSTS
@router.get("/", response_model=list[PostOut])
def get_all_posts(db: Session = Depends(get_db), current_user : User = Depends(get_current_user),  limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # # Equivalent to "SELECT * FROM posts"
    # posts = db.query(Post) # it actually returns a Query object (the raw SQL query), not the results yet
    # print(posts)
    # # The '%' symbols act as SQL wildcards for "anything before" and "anything after"
    # posts = posts.filter(Post.title.ilike(f"%{search}%")).limit(limit).offset(skip).all()  # Fetches results
    # return posts

    results = db.query(
        Post, 
        func.count(Vote.post_id).label("votes")
    ).join(
        Vote, Vote.post_id == Post.id, isouter=True
    ).group_by(
        Post.id
    ).all()
    
    return results

# 3. GET A SPECIFIC POST
@router.get("/{id}", response_model=PostResponse,)
def get_post(id: int, db: Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    # Equivalent to "SELECT * FROM posts WHERE id = {id}" 
    post = db.query(Post).filter(Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return post

# 4. UPDATE A POST
@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    # Update the dictionary of values
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    
    return post_query.first()  # Return the updated post

# 5. DELETE A POST
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    

    print(f"the user: {current_user.email} is trying to delete the post {id}")
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)