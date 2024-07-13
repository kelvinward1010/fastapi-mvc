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
    
class AuthInfo(BaseModel):
    email: EmailStr
    password: str

class UserChangePassword(BaseModel):
    email: EmailStr
    old_password: str
    password: str
    
class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    image: str | None = None
    position: str | None = None