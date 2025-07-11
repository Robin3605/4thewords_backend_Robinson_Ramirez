from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.db import get_session
from app.schemas.schemas import UserCreate, UserLogin, Token
from app.models.models import User
from app.auth.auth import get_current_user
from app.db.config import settings
from typing import List
from app.crud.users import login_user, user_register, get_all_users


router = APIRouter(tags=["Autenticación"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/token", response_model=Token)
def login(
    user_data: UserLogin, session: Session = Depends(get_session)
):
    return login_user(user_data, session)
    


@router.post("/users", response_model=User)
def register(user: UserCreate, session: Session = Depends(get_session)):
    return user_register(user, session)

@router.get("/users", response_model=List[User])
def get_users(session: Session = Depends(get_session)):
    return get_all_users(session)
    


@router.get("/me", response_model=User)
def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user