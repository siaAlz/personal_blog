from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime

Tag = Annotated[str, Field(min_length=3)]


# Models
class ArticleBase(BaseModel):
    author: str = Field(min_length=3, max_length=50)
    title: str = Field(min_length=3, max_length=50)
    content: str
    tags: list[Tag] = Field(default_factory=list)


class ArticleOut(ArticleBase):
    id: int = Field(ge=1)
    created_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
    )


# User Models
class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    is_active: bool = True


class UserIn(UserBase):
    password: str = Field(min_length=6, max_length=50)


class UserDb(UserBase):
    hashed_password: str = Field()


# Token Models


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
