from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from ..db import init_db
from ..schemas import user_schema
from ..services import user_service
from ..security import oauth2
from ..utils import init_util

db = init_db.users_collection

router = APIRouter(
    prefix="/user",
    tags=["User"],
)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user(id: str):
    try:
        ObjectId(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid user id")
    
    if not id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You need to provide all required information!")
    
    find_user = await user_service.find_user(id)
    
    return find_user

@router.put("/change-password", status_code=status.HTTP_200_OK)
async def change_password(infoChange: user_schema.UserChangePassword, user: dict = Depends(oauth2.get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticate!")
    
    if not infoChange.old_password or not infoChange.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You need to provide all required information!")
    
    if not init_util.verify(infoChange.old_password, user.get('password')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Old password not match with your account!")
    
    changed_password = await user_service.change_password_service(user['_id'], infoChange.password) 
    return changed_password


@router.put("/update-user/{id}", status_code=status.HTTP_200_OK)
async def update_user(id, infoChange: user_schema.UserUpdate, user: dict = Depends(oauth2.get_current_user)):
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticate!")
    
    if not id or not infoChange:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You need to provide all required information!")
    
    update = await user_service.change_user(id,infoChange)
    
    return update
    
    