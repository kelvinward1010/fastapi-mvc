from pydantic import BaseModel
from datetime import datetime


class CreatePostModel(BaseModel):
    topic: list[str]
    title: str
    authorID: str | int
    content: str
    description: str
    image_thumbnail: str
    
class CreatePostModelFinal(CreatePostModel):
    createdAt: datetime
    updatedAt: datetime