from pydantic import BaseModel, Field


# Models
class ArticleModel(BaseModel):
    id: int = Field(ge=1)
    author: str = Field(min_length=3, max_length=50)
    title: str = Field(min_length=3, max_length=50)
    content: str
