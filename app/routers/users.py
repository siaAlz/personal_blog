from fastapi import APIRouter, status
from ..services.users import create_user
from ..schemas.user import UserIn

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", status_code=status.HTTP_201_CREATED, tags=["public"])
async def signup_user(user: UserIn):
    # What if User already exists or is logged?
    return create_user(user)
