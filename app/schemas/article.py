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
