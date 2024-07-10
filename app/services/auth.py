from fastapi import Response
from bson import ObjectId
from datetime import datetime
from ..db import init_db
from ..utils import init_util
from ..schemas import user
from ..security import oauth2

db = init_db.users_collection

async def create_user(user_info):
    
    hashed_password = init_util.hash_password(user_info['password'])
    user_info['password'] = hashed_password
    
    data_to_create = user.CreateUserFinal(**user_info, createdAt=datetime.now(), updatedAt=datetime.now())
    
    if hashed_password:
        create_user = db.insert_one(dict(data_to_create))
        
    user_created = db.find_one({"_id": ObjectId(create_user.inserted_id)})
    
    converted = Entity(user_created)
    
    return {
        "status": 201,
        "message": "success",
        "data": converted
    }

async def login_server(id: str, response: Response) -> dict:
    
    access_token = oauth2.create_access_token(id)
    refresh_token = oauth2.create_refresh_token(id)
    
    response.set_cookie("access_token", access_token, httponly=True)
    
    return {
        "status": 200,
        "message": "success",
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


def Entity(user) -> dict:
    return {
        "_id": str(user["_id"]),
        "name": str(user["name"]),
        "email": user["email"],
        "password": user["password"],
        "image": user["image"],
        "position": user["position"],
        "createdAt": user["createdAt"],
        "updatedAt": user["updatedAt"],
    }