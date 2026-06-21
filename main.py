from typing import Annotated

from fastapi import FastAPI, Path, Query, status, HTTPException, Depends

from fastapi.security import OAuth2PasswordRequestForm

from models import ArticleBase, ArticleOut, UserIn
from utils import (
    load_articles,
    load_article,
    create_article,
    load_articles_by_tag,
    upload_article,
    get_user,
)
from dependencies import oauth2_scheme, get_urrent_user, get_current_active_user

app = FastAPI()


# Routes
@app.get("/", tags=["public"])
async def home(token: Annotated["str", Depends(oauth2_scheme)]):
    """
    This the home description. just for test!
    """
    return {"message": "Blog App", "token": token}


@app.get(
    "/articles",
    response_model=list[ArticleOut],
    tags=["public"],
    summary="Get all articles / by tags(optional)",
)
async def read_articles_by_tag(
    tag: Annotated[str | None, Query(min_length=3)] = None,
    _: Annotated[UserIn | None, Depends(get_urrent_user)] = None,
):
    if tag is None:
        return load_articles()
    articles = load_articles_by_tag(tag)
    return articles


@app.get(
    "/articles/{article_id}",
    response_model=ArticleOut,
    tags=["public"],
    summary="Get article by ID.",
)
async def read_article(article_id: Annotated[int, Path(ge=1)]):
    article = load_article(article_id)
    if article is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "article not found.")
    return article


@app.post(
    "/articles/create",
    status_code=status.HTTP_201_CREATED,
    tags=["admin"],
    summary="Create Article.",
)
async def post_article(
    article: ArticleBase,
    _: Annotated[UserIn | None, Depends(get_current_active_user)] = None,
):
    return create_article(article)


@app.put(
    "/articles/{article_id}",
    response_model=ArticleOut,
    status_code=status.HTTP_200_OK,
    tags=["admin"],
    summary="Update article.",
)
async def update_article(
    article_id: Annotated[int, Path(ge=1)], updated_article: ArticleBase
):

    uploaded_article = upload_article(article_id, updated_article)
    if uploaded_article is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "article not found.")
    return uploaded_article


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = get_user(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password.")
    user = UserIn(**user_dict)
    hashed_password = form_data.password  # Most hash it!
    if not user.password == hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password.",
        )
    return {"access_token": user.username, "token_type": "bearer"}
