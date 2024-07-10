from fastapi import HTTPException, status
from bson import ObjectId
from datetime import datetime
from ..db import init_db
from ..utils import init_util
from ..schemas import entity



db = init_db.users_collection

async def find_user(id: str) -> dict:
    
    user = db.find_one({"_id": ObjectId(id)})
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found user with id: {id}")
    
    return {
        "status": 200,
        "message": "success",
        "data": entity.EntityUser(user)
    }
    
async def change_password_service(id, password: str) -> dict:
    
    hashed_password = init_util.hash_password(password)
    
    db.find_one_and_update({"_id": ObjectId(id)},{
        "$set": dict(password = hashed_password)
    })
    
    return {
        "status": 200,
        "message": "success",
        "data": "Changed password"
    }