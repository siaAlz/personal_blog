from typing import Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from utils import get_user
from models import UserIn

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_urrent_user(token: Annotated[str, Depends((oauth2_scheme))]) -> UserIn:
    # Decode token then
    user = get_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserIn(**user)


def get_current_active_user(current_user: Annotated[UserIn, Depends(get_urrent_user)]):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User"
        )
