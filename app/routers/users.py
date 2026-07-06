from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import models
from app.dependencies import get_current_user, get_db
from app.services.users import (
    create_user,
    delete_user_service,
    get_users_service,
    update_user_service,
)
from app.schemas.user import UserIn, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
def get_users(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    return get_users_service(db, current_user)


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def signup_user(db: Annotated[Session, Depends(get_db)], user: UserIn):
    return create_user(db, user)


@router.patch("/update", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_user(
    db: Annotated[Session, Depends(get_db)],
    user_data: UserUpdate,
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    return update_user_service(db, user_data, current_user)


@router.delete("/update", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    return delete_user_service(db, current_user)
