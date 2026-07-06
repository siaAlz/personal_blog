from collections.abc import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.schemas.article import ArticleCreate, ArticleResponse


def load_articles(db: Session) -> Sequence[models.Article]:
    res = db.execute(select(models.Article))
    articles = res.scalars().all()
    return articles


def load_article(db: Session, article_id: int) -> models.Article:
    article = db.get(models.Article, article_id)
    if article is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Article not found.")
    return article


def load_articles_by_tag(db: Session, tag: str) -> Sequence[models.Article]:
    res = db.execute(select(models.Article).where(models.Article.tags.contains([tag])))
    articles = res.scalars().all()
    return articles


def create_article(db: Session, article: ArticleCreate, current_user: models.User):

    new_article = models.Article(
        title=article.title,
        body=article.body,
        tags=article.tags,
        user_id=current_user.id,
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


#
def update_article_service(
    db: Session,
    article_id: int,
    updated_article: ArticleCreate,
    current_user: models.User,
) -> models.Article:

    article = db.get(models.Article, article_id)

    if article is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Article not found.")

    if article.author.id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Access not granted.")
    article.title = updated_article.title
    article.tags = updated_article.tags
    article.body = updated_article.body

    db.commit()
    db.refresh(article)
    return article
