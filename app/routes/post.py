from fastapi import APIRouter, HTTPException, status, Response, Depends
from bson import ObjectId
from ..db import init_db
from ..schemas import post_schema, entity
from ..services import post_service
from ..security import oauth2
from ..utils import init_util

db = init_db.posts_collection

router = APIRouter(
    prefix="/post",
    tags=["Post"],
)

@router.get("/all_posts")
async def get_all_posts():
    posts = entity.EntinyListPost(db.find())
    return posts

@router.get("/search_post")
async def get_search_posts(query: post_schema.SearchModel):
    postsfinal = await post_service.search_post_service(query.title, query.topic)
    return postsfinal

@router.get("/newest_posts")
async def get_newest_posts(count: int):
    newest_posts = entity.EntinyListPost(db.find().sort("createdAt", -1).limit(count))
    return newest_posts

@router.post("/create_post", status_code=status.HTTP_201_CREATED)
async def create_post(infoCreate: post_schema.CreatePostModel, user: dict = Depends(oauth2.get_current_user)):
    
    infoPost = infoCreate.model_dump()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticate!")
    
    if not infoPost['authorID'] or not infoPost["title"] or not infoPost['description'] or not infoPost['content']:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="You need to provide all required information!")
    
    newPost = await post_service.create_post(infoPost)
    
    return newPost

@router.get("/{id}")
async def find_post(id):
    if not id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing id!")
    
    post = await post_service.get_post_follow_id(id)
    return post

@router.put("/update/{id}")
async def update_post(id, infoChange: post_schema.UpdatePostModel, user: dict = Depends(oauth2.get_current_user)):
    
    infoPost = infoChange.model_dump()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticate!")
    
    if not infoPost['authorID'] or not infoPost["title"] or not infoPost['description'] or not infoPost['content']:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="You need to provide all required information!")
    
    find_post = db.find_one({"_id": ObjectId(id)})

    if not find_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post to update!")
    
    post_updated = await post_service.change_post(id, infoChange)
    
    return post_updated