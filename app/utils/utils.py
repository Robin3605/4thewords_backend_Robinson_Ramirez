# from sqlmodel import  Session
# from app.db.db import get_session
# from fastapi import  Depends, Request
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import Query
from typing import Optional

# class QueryParams:
#     # skip: int = 0,
#     # limit: int = 100,
#     title: str = None,
#     category_id: int = None,
#     province_id: int = None,
#     canton_id: int = None,
#     district_id: int = None,
#     start_date: str = None,
#     end_date: str = None,
#     # request: Request = None,
#     # session: Session = Depends(get_session),

class QueryParams(BaseModel):
    title: Optional[str] = None
    category_id: Optional[int] = None
    province_id: Optional[int] = None
    canton_id: Optional[int] = None
    district_id: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
