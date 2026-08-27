import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
from .schemas import TokenData
from jwt.exceptions import PyJWTError, InvalidTokenError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer   
from .databases import get_db
from sqlalchemy.orm import Session
from .models import User

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY')

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        'exp': expire
    })

    print("BR)_TO_ENCODE",to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)   
        print("PayLOAD: ",payload)
        user_id: str = payload.get('user_id')

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(id=user_id)

    except InvalidTokenError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="couldn't validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    print("BRO:",User.id)
    print("BRO:",token.id)
    user = db.query(User).filter(User.id == token.id).first()
    return user