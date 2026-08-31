from models import User
from schemas import UserResponse, UserCreate
from utils import hash_password
from databases import get_db
from fastapi import status, Depends, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session 



router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pwd = hash_password(user.password)
    user.password = hashed_pwd
    new_user = User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return users

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.id == id)
    user = user_query.first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found!"
        )

    return user
    

@router.put('/{id}', response_model=UserResponse)
def update_user(id: int, updated_user: UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.id == id)
    user = user_query.first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found!"
        )

    hashed_pwd = hash_password(updated_user.password)
    updated_user.password = hashed_pwd
    
    user_query.update(updated_user.model_dump(), synchronize_session=False)

    db.commit()

    db.refresh(user)

    return user

@router.delete('/{id}')
def delete_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.id == id)
    user = user_query.first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found!"
        )
    user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)