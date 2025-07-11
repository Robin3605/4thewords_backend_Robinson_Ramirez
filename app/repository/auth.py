from sqlmodel import Session, select
from app.models.models import User
from app.utils.utils import verify_password
from app.schemas.schemas import TokenData

def authenticate_user(email: str, password: str, session: Session):
    user = get_users_email(email, session)
    if user is None:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_users_email(email: str, session: Session):
    user =  session.exec(select(User).where(User.email == email)).first() 
    if not user:
        return None
    return user


def user_with_tocken(token_data: TokenData, session: Session):
    user =  session.exec(select(User).where(User.email == token_data.email)).first()
    if user is None:
        return None
    return user