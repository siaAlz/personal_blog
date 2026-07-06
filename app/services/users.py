from collections.abc import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.core.security import DUMMY_HASH, get_password_hash, verify_password
from app.schemas.user import UserDb, UserIn


def create_user(db: Session, user: UserIn):
    username_exists = (
        db.execute(select(models.User).where(models.User.username == user.username))
        .scalars()
        .first()
    )
    email_exists = (
        db.execute(select(models.User).where(models.User.email == user.email))
        .scalars()
        .first()
    )
    if username_exists or email_exists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Username or Email already exists."
        )

    hashed_password = get_password_hash(user.password)
    user_db = UserDb(**user.model_dump(), hashed_password=hashed_password)
    new_user = models.User(**user_db.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, username) -> models.User | None:
    user = (
        db.execute(select(models.User).where(models.User.username == username))
        .scalars()
        .first()
    )

    return user


def get_users_service(db: Session, current_user) -> Sequence[models.User]:
    users = db.execute(select(models.User)).scalars().all()
    return users


def authenticate_user(db: Session, username: str, password: str) -> models.User | bool:
    user = get_user(db, username)
    if user is None:
        verify_password(password, DUMMY_HASH)
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user
