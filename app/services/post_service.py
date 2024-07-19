from fastapi import HTTPException, status
from bson import ObjectId
from datetime import datetime
from ..db import init_db
from ..schemas import entity, post_schema



db = init_db.posts_collection
dbuser = init_db.users_collection

async def search_posts_service(title, topic, limit, neworold) -> dict:
    
    query = {}
    if title or topic:
        query["$or"] = []
        if title:
            query["$or"].append({"title": {"$regex": title, "$options": "i"}})
        if topic:
            query["$or"].append({"topic": {"$in": topic}})
    
    searched_posts = db.find(query).limit(int(limit)).sort("createdAt", int(neworold))
    
    posts = entity.EntinyListPost(list(searched_posts))
    
    return {
        "status": 200,
        "message": "success",
        "data": posts
    }

async def search_topics_posts(topic, limit, neworold) -> dict:
    query = {}
    if topic:
        query["$or"] = []
        query["$or"].append({"topic": {"$in": topic}})
        
    searched_posts = db.find(query).limit(int(limit)).sort("createdAt", neworold)
    
    posts = entity.EntinyListPost(list(searched_posts))
    
    return {
        "status": 200,
        "message": "success",
        "data": posts
    }

async def search_your_posts(id, title) -> dict:
    query = {}
    if title:
        query["$or"] = []
        query["$or"].append({"title": {"$regex": title, "$options": "i"}})
    if id:
        query["authorID"] = id
        
    searched_posts = db.find(query).sort("createdAt", -1)
    
    posts = entity.EntinyListPost(list(searched_posts))
    
    return {
        "status": 200,
        "message": "success",
        "data": posts
    }

async def your_posts_favorites(ids_posts) -> dict:
    
    posts_favorites = entity.EntinyListPost(db.find_one({"_id": ObjectId(id_post)}) for id_post in ids_posts)
    
    return {
        "status": 200,
        "message": "success",
        "data": posts_favorites
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
    
async def get_postId(id) -> dict:
    
    data_post = db.find_one({"_id": ObjectId(id)})
    if not data_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    
    return {
        "status": 200,
        "message": "success",
        "data": entity.EntityPost(data_post)
    }
    
async def change_post(id, infoChange) -> dict:
    
    db.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(infoChange, updatedAt=datetime.now())
    })
    
    post_after_update = db.find_one({"_id": ObjectId(id)})
    
    return {
        "status": 200,
        "message": "success",
        "data": entity.EntityPost(post_after_update)
    }
    
async def like_post_service(id, user, like, post):
    
    id_user = user["_id"]
    favoritesposts: list = user['favoritesposts']
    
    likes_in_post: list = post['likes']
    isReadyLike = False
    for i in likes_in_post:
        if str(i) == str(id_user):
            isReadyLike = True
        else:
            isReadyLike = False
    
    if like.isLike == 1:
        if isReadyLike == True:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"You're already like this post!")
        
        favoritesposts.append(id)
        likes_in_post.append(id_user)
        db.find_one_and_update({"_id": ObjectId(id)},{"$set": dict(post)})
        dbuser.find_one_and_update({"_id": ObjectId(id_user)},{"$set": {"favoritesposts": favoritesposts}})
        
        return {
            "status": 200,
            "message": "success",
            "data": entity.EntityPost(post)
        }
        
    if like.isLike == 0:
        if isReadyLike == False:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"You haven't liked this post!")
        
        favoritesposts.remove(id)
        likes_in_post.remove(id_user)
        db.find_one_and_update({"_id": ObjectId(id)},{"$set": dict(post)})
        dbuser.find_one_and_update({"_id": ObjectId(id_user)},{"$set": {"favoritesposts": favoritesposts}})
        
        return {
            "status": 200,
            "message": "success",
            "data": entity.EntityPost(post)
        }   
    