from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..databases import get_db
from ..schemas import UserLogin
from ..models import User
from ..utils import hash_password, verify_password
from ..oauth2 import create_access_token

router = APIRouter(tags={'Authentication'})

@router.post('/login')
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email")

    if (not verify_password(user.password, user_credentials.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid password')


    return {
        'token': create_access_token({'user_id': user_credentials.email})
    }


    
    