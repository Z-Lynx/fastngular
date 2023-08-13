from typing import Optional
from pydantic import BaseModel
    
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from apps.demo.models import NguoiDung
from apps.utils.auth import get_password_hash, verify_password
from apps.schemas.user import UserCreate, UserUpdate


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_user(db: Session, username: str):
    return db.query(NguoiDung).filter(NguoiDung.email == username).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = NguoiDung(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: NguoiDung, user: UserUpdate):
    if user.password:
        hashed_password = get_password_hash(user.password)
        db_user.password = hashed_password
    db_user.username = user.username
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user