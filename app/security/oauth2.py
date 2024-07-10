from jose import JWSError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId
from typing import Annotated
from ..core.config import settings 
from ..schemas import token, entity
from ..db import init_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY = settings.SECRETKEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESSTOKENEXPIREMINUTES

def create_access_token(id: str) -> str:
    to_encode = {"id": id}
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(id: str) -> str:
    to_encode = {"id": id}
    expire = datetime.now() + timedelta(days=30)  # Refresh token expires in 30 days
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(tokenStr: str, credentials_exception) -> token.TokenData:
    try:
        payload = jwt.decode(tokenStr, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")
        if not id:
            raise credentials_exception
        token_data = token.TokenData(id=str(id))
    except JWSError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token has an expired signature!",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return token_data

def refresh_access_token(refresh_token: str) -> str:
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")
        if not id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        # You can add additional checks here, such as verifying if the user exists in the database.
        new_access_token = create_access_token(id)
        return new_access_token
    except JWSError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )

async def get_current_user(tokenStr: Annotated[str, Depends(oauth2_scheme)]):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    token_data = verify_access_token(tokenStr, credentials_exception)
    user = init_db.users_collection.find_one({"_id": ObjectId(token_data.id)})
    
    return entity.EntityUser(user)
