from collections.abc import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, session
from starlette.status import HTTP_400_BAD_REQUEST

from app import models
from app.core.security import DUMMY_HASH, get_password_hash, verify_password
from app.schemas.user import UserDb, UserIn, UserUpdate


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


def update_user_service(
    db: Session, user_data: UserUpdate, current_user: models.User
) -> models.User:

    if user_data.username is not None and user_data.username != current_user.username:
        existing_user = (
            db.execute(
                select(models.User).where(models.User.username == user_data.username)
            )
            .scalars()
            .first()
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists.",
            )
    if user_data.email is not None and user_data.email != current_user.email:
        existing_user = (
            db.execute(select(models.User).where(models.User.email == user_data.email))
            .scalars()
            .first()
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists.",
            )
    updated_data = user_data.model_dump(exclude_unset=True)
    for field, value in updated_data.items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user


def delete_user_service(db: Session, current_user: models.User):
    db.delete(current_user)
    db.commit()


def authenticate_user(db: Session, username: str, password: str) -> models.User | bool:
    user = get_user(db, username)
    if user is None:
        verify_password(password, DUMMY_HASH)
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user
