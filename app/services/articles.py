from collections.abc import Sequence
import re

from sqlalchemy import select
from sqlalchemy.engine import result
from sqlalchemy.orm import Session

from app import models
from app.routers import articles
from app.schemas.article import ArticleCreate, ArticleResponse
from app.db.db import initiate_db, load_db, save_db

DB_PATH = initiate_db()
db = load_db(DB_PATH)


def load_articles(db: Session) -> Sequence[models.Article]:
    result = db.execute(select(models.Article))
    articles = result.scalars().all()
    return articles
    # return [ArticleBase(**a) for a in articles]


def load_article(article_id: int) -> ArticleOut | None:
    articles = load_articles()
    for a in articles:
        if a.id == article_id:
            return a


def create_article(article: ArticleBase):
    articles = load_articles()
    articles.sort(key=lambda article: article.id)
    last_id = articles[-1].id

    new_article = ArticleOut(
        **article.model_dump(),
        id=last_id + 1,
    )

    articles.append(new_article)
    db["Articles"] = [a.model_dump() for a in articles]
    save_db(db, DB_PATH)
    return new_article


def load_articles_by_tag(db: Session, tag: str) -> list[ArticleOut]:
    articles = load_articles(db)

    articles_by_tag = [a for a in articles if tag in a.tags]
    return articles_by_tag


def upload_article(article_id: int, updated_article: ArticleBase) -> ArticleOut | None:
    articles = load_articles()

    for i, article in enumerate(articles):
        if article.id == article_id:
            articles[i] = ArticleOut(
                id=articles[i].id,
                **updated_article.model_dump(),
                created_at=articles[i].created_at,
            )

            db["Articles"] = [a.model_dump() for a in articles]
            save_db(db, DB_PATH)
            return articles[i]
    return None
