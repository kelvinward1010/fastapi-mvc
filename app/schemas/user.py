from pydantic import BaseModel, EmailStr
from typing import Optional

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str
    image: str | None = None
    position: str | None = None