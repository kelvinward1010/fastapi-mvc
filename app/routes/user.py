from fastapi import APIRouter, HTTPException, status, Response
from ..db import init_db
from ..schemas import user
from ..services.user import create_user

db = init_db.users_collection

router = APIRouter(
    prefix="/user",
    tags=["User"],
)

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def add_user(payload: user.CreateUser):
    user = payload.model_dump()
    if not user['name'] or not user['email'] or not user['password']:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="You need to provide all required information!")
    
    exist_email = db.find_one({"email": user["email"]})
    if exist_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exist"
        )
        
    new_user = await create_user(user)
    return new_user

    