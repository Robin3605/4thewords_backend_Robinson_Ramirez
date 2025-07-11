from sqlmodel import select, Session
from app.schemas.schemas import UserCreate
from sqlmodel import  Session
from app.models.models import  User
from fastapi import  HTTPException
from app.utils.utils import get_password_hash




def register(user: UserCreate, session: Session ):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user  


def get_users_db(session: Session ):
    return session.exec(select(User)).all()
