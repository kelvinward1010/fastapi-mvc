from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str
    image: str | None = None
    position: str | None = None

class CreateUserFinal(CreateUser):
    createdAt: datetime
    updatedAt: datetime