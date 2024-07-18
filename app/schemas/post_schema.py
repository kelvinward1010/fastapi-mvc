from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class CreatePostModel(BaseModel):
    topic: list[str]
    title: str
    authorID: str | int
    content: str
    description: str
    image_thumbnail: str
    likes: list[str]
    
class CreatePostModelFinal(CreatePostModel):
    createdAt: datetime
    updatedAt: datetime
    
class SearchPostsModel(BaseModel):
    topic: list[str] = None 
    title: str = None
    limit: int = None
    neworold: int = None

class UpdatePostModel(BaseModel):
    topic: list[str]
    title: str
    authorID: str | int
    content: str
    description: str
    image_thumbnail: str
    likes: list[str]
    
class Like(BaseModel):
    isLike: Literal[0,1]