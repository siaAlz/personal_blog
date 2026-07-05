from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.schemas.article import ArticleBase, ArticleOut
from app.schemas.user import UserBase
from app.services.articles import (
    create_article,
    load_article,
    load_articles,
    load_articles_by_tag,
    upload_article,
)
from app.dependencies import get_current_user, get_current_active_user

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get(
    "/",
    response_model=list[ArticleOut],
    tags=["public"],
    summary="Get all articles / by tags(optional)",
)
async def read_articles_by_tag(
    tag: Annotated[str | None, Query(min_length=3)] = None,
):
    if tag is None:
        return load_articles()
    articles = load_articles_by_tag(tag)
    return articles


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    tags=["admin"],
    summary="Create Article.",
)
async def post_article(
    article: ArticleBase,
    _: Annotated[UserBase | None, Depends(get_current_active_user)] = None,
):
    return create_article(article)


@router.get(
    "/{article_id}",
    response_model=ArticleOut,
    tags=["public"],
    summary="Get article by ID.",
)
async def read_article(article_id: Annotated[int, Path(ge=1)]):
    article = load_article(article_id)
    if article is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "article not found.")
    return article


@router.put(
    "/{article_id}",
    response_model=ArticleOut,
    status_code=status.HTTP_200_OK,
    tags=["admin"],
    summary="Update article.",
)
async def update_article(
    article_id: Annotated[int, Path(ge=1)],
    updated_article: ArticleBase,
    _: Annotated[UserBase | None, Depends(get_current_user)] = None,
):

    uploaded_article = upload_article(article_id, updated_article)
    if uploaded_article is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "article not found.")
    return uploaded_article
