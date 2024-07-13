from fastapi import Response
from bson import ObjectId
from datetime import datetime
from ..db import init_db
from ..utils import init_util
from ..schemas import user_schema, entity
from ..security import oauth2

db = init_db.users_collection

async def create_user(user_info):
    
    hashed_password = init_util.hash_password(user_info['password'])
    user_info['password'] = hashed_password
    
    data_to_create = user_schema.CreateUserFinal(**user_info, createdAt=datetime.now(), updatedAt=datetime.now())
    
    if hashed_password:
        created_user = db.insert_one(dict(data_to_create))
        
    user_created = db.find_one({"_id": ObjectId(created_user.inserted_id)})
    
    converted = entity.EntityUser(user_created)
    
    return {
        "status": 201,
        "message": "success",
        "data": converted
    }

async def login_server(id: str,user, response: Response) -> dict:
    
    access_token = oauth2.create_access_token(id)
    refresh_token = oauth2.create_refresh_token(id)
    
    response.set_cookie("access_token", access_token, httponly=True)
    
    return {
        "status": 200,
        "message": "success",
        "user": entity.EntityUser(user),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }