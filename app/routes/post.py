from fastapi import APIRouter, HTTPException, status, Response, Depends
from bson import ObjectId
from ..db import init_db
from ..schemas import post_schema
from ..services import post_service
from ..security import oauth2
from ..utils import init_util

db = init_db.posts_collection

router = APIRouter(
    prefix="/post",
    tags=["Post"],
)

@router.post("/create_post", status_code=status.HTTP_201_CREATED)
async def create_post(infoCreate: post_schema.CreatePostModel, user: dict = Depends(oauth2.get_current_user)):
    
    infoPost = infoCreate.model_dump()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticate!")
    
    if not infoPost['authorID'] or not infoPost["title"] or not infoPost['description'] or not infoPost['content']:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="You need to provide all required information!")
    
    newPost = await post_service.create_post(infoPost)
    
    return newPost