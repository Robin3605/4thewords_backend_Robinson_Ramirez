from sqlmodel import  Session
from app.schemas.schemas import UserLogin, UserCreate
from fastapi import  HTTPException, status
from datetime import timedelta
from app.db.config import settings
from app.auth.jwt_handler import create_access_token
from fastapi.responses import JSONResponse
from app.repository.users import register, get_users_db
from app.auth.auth import authenticate_user



def login_user(
    user_data: UserLogin, session: Session ):
    user = authenticate_user(user_data.email, user_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    
    response = JSONResponse(content={
        "access_token": access_token,
        "token_type": "bearer"
    })

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        max_age=1800,
        secure=False
    )

    return response  

def user_register(user: UserCreate, session: Session):
    return register(user, session)

def get_all_users(session: Session):
    return get_users_db(session)