import os
from typing import Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from utils import get_user
from models import TokenData, UserBase

import jwt
from jwt.exceptions import InvalidTokenError

SECRET_KEY = os.getenv("SECRET_KEY")
ALOGORITHM = os.getenv("ALOGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_urrent_user(token: Annotated[str, Depends((oauth2_scheme))]) -> UserBase:

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, ALOGORITHM)
        username = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise credential_exception

    user = get_user(token_data.username)

    if not user:
        raise credential_exception
    return UserBase(**user)


def get_current_active_user(
    current_user: Annotated[UserBase, Depends(get_urrent_user)],
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User"
        )
