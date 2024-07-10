from fastapi import APIRouter, HTTPException, status, Response, Depends
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

@router.get("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def get_user(id: str):
    if not id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="You need to provide all required information!")
    
    find_user = await user_service.find_user(id)
    
    return find_user

@router.put("/change_password/{id}", status_code=status.HTTP_202_ACCEPTED)
async def change_password(id, infoChange: user_schema.UserChangePassword, user: dict = Depends(oauth2.get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticate!")
    
    if not id or not infoChange:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="You need to provide all required information!")
    
    user_exist = db.find_one({"_id": ObjectId(id)})
    
    if not user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found user with id: {id} to update!")
    elif not init_util.verify(infoChange.old_password, user_exist.get('password')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Old password not match with your account!")
    
    changed_password = await user_service.change_password_service(id, infoChange.password) 
    return changed_password