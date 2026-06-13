from typing import Annotated

from fastapi import FastAPI, Path, Query, status, HTTPException
from models import ArticleModel
from utils import load_articles, load_article, create_article, load_articles_by_tag

app = FastAPI()


# Routes
@app.get("/")
async def home():
    return {"message": "Blog App"}


# @app.get("/articles", response_model=list[ArticleModel])
# async def read_articles():
#    return load_articles()


@app.get("/articles/{article_id}", response_model=ArticleModel)
async def read_article(article_id: Annotated[int, Path(ge=1)]):
    article = load_article(article_id)
    if article is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "article not found.")
    return article


@app.get("/articles", response_model=list[ArticleModel])
async def read_articles_by_tag(tag: Annotated[str | None, Query(min_length=3)] = None):
    articles = load_articles_by_tag(tag)
    return articles


@app.post("/articles/create", status_code=status.HTTP_201_CREATED)
async def post_article(article: ArticleModel):
    return create_article(article)
