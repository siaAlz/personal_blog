from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated
from datetime import datetime

from app.schemas.user import UserResponse

Tag = Annotated[str, Field(min_length=3)]


class ArticleBase(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    content: str
    tags: list[Tag] = Field(default_factory=list)


class ArticleCreate(ArticleBase):
    user_id: int  # Temporary?


class ArticleResponse(ArticleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(ge=1)
    user_id: int
    date_published: datetime
    author: UserResponse  # ?
