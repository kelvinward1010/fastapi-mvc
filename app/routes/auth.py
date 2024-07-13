from fastapi import APIRouter, HTTPException, status, Response
from ..db import init_db
from ..schemas import user_schema
from ..utils import init_util
from ..services.auth import create_user, login_server
from ..security.oauth2 import refresh_access_token

db = init_db.users_collection

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(payload: user_schema.CreateUser):
    userinfo = payload.model_dump()
    if not userinfo['name'] or not userinfo['email'] or not userinfo['password']:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="You need to provide all required information!")
    
    exist_email = db.find_one({"email": userinfo["email"]})
    if exist_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exist"
        )
        
    new_user = await create_user(userinfo)
    return new_user


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(payload: user_schema.AuthInfo, response: Response):
    user_info = payload.model_dump()
    if not user_info['email'] or not user_info['password']:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="You need to provide all required information!")
    
    exist_account = db.find_one({"email": user_info["email"]})
    if not exist_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't already exist"
        )
    
    hashed_password = exist_account.get('password')
    
    if not init_util.verify(user_info['password'], hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Password!")
    
    loginSV = await login_server(str(exist_account.get('_id')), response=response)
    return loginSV


@router.post('/refresh-token', status_code=status.HTTP_200_OK)
async def refresh_token(refreshtokenStr: str, response: Response):
    if not refreshtokenStr:
        return {"error": "Refresh token is missing."}

    new_access_token = refresh_access_token(refreshtokenStr)
    
    response.set_cookie("access_token", new_access_token, httponly=True)
    
    return {
        "status": 200,
        "message": "success",
        "data": {
            "token": new_access_token
        }
    }

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {
        "status": 200,
        "message": "success",
    }
