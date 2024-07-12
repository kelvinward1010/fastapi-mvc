from fastapi import HTTPException, status
from bson import ObjectId
from datetime import datetime
from ..db import init_db
from ..utils import init_util
from ..schemas import entity, post_schema



db = init_db.posts_collection

async def create_post(infoCreate) -> dict:
    
    data_to_create = post_schema.CreatePostModelFinal(**infoCreate, createdAt=datetime.now(), updatedAt=datetime.now())
    
    created_post = db.insert_one(dict(data_to_create))

    post_created = db.find_one({"_id": ObjectId(created_post.inserted_id)})
    
    converted = entity.EntityPost(post_created)
    
    return {
        "status": 200,
        "message": "success",
        "data": converted
    }