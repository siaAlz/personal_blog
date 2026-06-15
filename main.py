from typing import Annotated

from fastapi import FastAPI, Path, Query, status, HTTPException
from models import ArticleBase, ArticleModel
from utils import (
    load_articles,
    load_article,
    create_article,
    load_articles_by_tag,
    upload_article,
)

app = FastAPI()


# Routes
@app.get("/")
async def home():
    return {"message": "Blog App"}


@app.get("/articles", response_model=list[ArticleModel])
async def read_articles_by_tag(tag: Annotated[str | None, Query(min_length=3)] = None):
    if tag is None:
        return load_articles()
    articles = load_articles_by_tag(tag)
    return articles


@app.get("/articles/{article_id}", response_model=ArticleModel)
async def read_article(article_id: Annotated[int, Path(ge=1)]):
    article = load_article(article_id)
    if article is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "article not found.")
    return article


@app.post("/articles/create", status_code=status.HTTP_201_CREATED)
async def post_article(article: ArticleModel):
    return create_article(article)


@app.put(
    "/articles/{article_id}",
    response_model=ArticleBase,
    status_code=status.HTTP_200_OK,
)
async def update_article(
    article_id: Annotated[int, Path(ge=1)], updated_article: ArticleBase
):

    uploaded_article = upload_article(article_id, updated_article)
    if uploaded_article is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "article not found.")
    return uploaded_article
