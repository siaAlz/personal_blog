from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import models
from app.dependencies import get_current_user, get_db
from app.services.users import create_user, get_users_service
from app.schemas.user import UserIn, UserResponse

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
