from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.db.db import get_session
from app.schemas.schemas import TokenData
from jose import JWTError, jwt
from app.db.config import settings
from app.repository.auth import get_users_email, user_with_tocken
from app.utils.utils import verify_password

# Enruta el login a /token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(email: str, password: str, session: Session):
    user = get_users_email(email, session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Si el token no vino por header, buscarlo en cookies
    if not token:
        token = request.cookies.get("access_token")
        if token and token.startswith("Bearer "):
            token = token.split(" ")[1]

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = user_with_tocken(token_data, session)
    if user is None:
        raise credentials_exception
    return user