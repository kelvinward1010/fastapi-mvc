from fastapi import HTTPException, status
from bson import ObjectId
from datetime import datetime
from ..db import init_db
from ..utils import init_util
from ..schemas import entity, post_schema



db = init_db.posts_collection

async def search_post_service(title, topic) -> dict:
    
    query = {}
    if title or topic:
        query["$or"] = []
        if title:
            query["$or"].append({"title": {"$regex": title, "$options": "i"}})
        if topic:
            query["$or"].append({"topic": {"$in": topic}})
    
    posts = entity.EntinyListPost(list(db.find(query)))
    
    return {
        "status": 200,
        "message": "success",
        "data": posts
    }

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
    
async def get_post_follow_id(id: str) -> dict:
    
    item = db.find_one({"_id": ObjectId(id)})
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    
    return {
        "status": 200,
        "message": "success",
        "data": item
    }
    
async def change_post(id,infoChange) -> dict:
    
    db.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(infoChange)
    })
    
    post_after_update = db.find_one({"_id": ObjectId(id)})
    
    return {
        "status": 200,
        "message": "success",
        "data": entity.EntityPost(post_after_update)
    }