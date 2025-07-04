from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db.db import get_session
from app.schemas.schemas import UserCreate, UserLogin, Token
from app.models.models import User
from app.auth.auth import authenticate_user, create_access_token, get_password_hash
from datetime import timedelta
from fastapi.responses import JSONResponse
from app.db.config import settings
from typing import List

router = APIRouter(tags=["Autenticación"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/login", response_model=Token)
def login(
    form_data: UserLogin,
    session: Session = Depends(get_session)
):
    user = authenticate_user(form_data.email, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    # Respuesta con token y cookie
    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        samesite="Lax",
        max_age=1800,
        secure=False  # cambia a True si usas HTTPS
    )
    return response

@router.post("/users", response_model=User)
def register(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user  # esto devuelve el usuario realmente guardado

@router.get("/users", response_model=List[User])
def get_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()