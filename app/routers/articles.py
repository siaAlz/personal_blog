from operator import mod
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from app import models
from app.dependencies import get_current_active_user, get_current_user, get_db
from app.schemas import article
from app.schemas.article import ArticleCreate, ArticleResponse
from app.services.articles import (
    create_article,
    load_article,
    load_articles,
    load_articles_by_tag,
    update_article_service,
)

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get(
    "/",
    response_model=list[ArticleResponse],
    summary="Get all articles / by tags(optional)",
)
async def read_articles_by_tag(
    db: Annotated[Session, Depends(get_db)],
    tag: Annotated[str | None, Query(min_length=3)] = None,
):
    if tag is None:
        return load_articles(db)
    articles = load_articles_by_tag(db, tag)
    return articles


@router.get(
    "/{article_id}",
    response_model=ArticleResponse,
    summary="Get article by ID.",
)
async def get_article(
    db: Annotated[Session, Depends(get_db)], article_id: Annotated[int, Path(ge=1)]
):
    return load_article(db, article_id)


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    summary="Create Article.",
    response_model=ArticleResponse,
)
async def post_article(
    db: Annotated[Session, Depends(get_db)],
    article: ArticleCreate,
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    return create_article(db, article, current_user)


@router.put(
    "/update/{article_id}",
    response_model=ArticleResponse,
    status_code=status.HTTP_200_OK,
    summary="Update article.",
)
async def update_article(
    db: Annotated[Session, Depends(get_db)],
    article_id: Annotated[int, Path(ge=1)],
    updated_article: ArticleCreate,
    current_user: Annotated[models.User, Depends(get_current_user)],
):

    return update_article_service(db, article_id, updated_article, current_user)


@router.delete("/delete/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    db: Annotated[Session, Depends(get_db)],
    article_id: Annotated[int, Path(ge=1)],
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    return delete_article_service(db, article_id, current_user)
