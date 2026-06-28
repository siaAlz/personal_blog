from datetime import timedelta
from typing import Annotated


from fastapi import FastAPI, Path, Query, status, HTTPException, Depends

from fastapi.security import OAuth2PasswordRequestForm

from models import ArticleBase, ArticleOut, Token, UserBase, UserIn
from utils import (
    authenticate_user,
    create_access_token,
    create_user,
    load_articles,
    load_article,
    create_article,
    load_articles_by_tag,
    upload_article,
    get_user,
)
from dependencies import oauth2_scheme, get_urrent_user, get_current_active_user

# ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
    _: Annotated[UserBase | None, Depends(get_current_active_user)] = None,
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
    article_id: Annotated[int, Path(ge=1)],
    updated_article: ArticleBase,
    _: Annotated[UserBase | None, Depends(get_urrent_user)] = None,
):

    uploaded_article = upload_article(article_id, updated_article)
    if uploaded_article is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "article not found.")
    return uploaded_article


@app.post("/users/signup", status_code=status.HTTP_201_CREATED, tags=["public"])
async def signup_user(user: UserIn):
    # What if User already exists or is logged?
    return create_user(user)


@app.post("/token", tags=["public"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
