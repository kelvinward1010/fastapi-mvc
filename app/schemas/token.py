from pydantic import BaseModel
from typing import Optional

class AccessToken(BaseModel):
    access_token: str

class RefreshToken(BaseModel):
    refresh_token: str

class TokenData(BaseModel):
    id: Optional[str] = None