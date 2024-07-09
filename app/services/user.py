from fastapi import APIRouter, HTTPException, status, Response
from ..db import init_db
from bson import ObjectId


db = init_db.users_collection

async def create_user(user):
    created_user = db.insert_one(dict(user))
    user_ok = db.find_one({"_id": ObjectId(created_user.inserted_id)})
    convert = Entity(user_ok)
    
    return {
        "status": 201,
        "message": "success",
        "data": convert
    }



def Entity(user) -> dict:
    return {
        "_id": str(user["_id"]),
        "name": str(user["name"]),
        "email": user["email"],
        "password": user["password"],
        "image": user["image"],
        "position": user["position"],
    }