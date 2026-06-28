from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from pwdlib import PasswordHash

from models import ArticleBase, ArticleOut, UserDb, UserIn
from db import initiate_db, load_db, save_db

import os
import jwt

# DB
DB_PATH = initiate_db()
db = load_db(DB_PATH)


def load_articles() -> list[ArticleOut]:
    articles = db["Articles"]
    return [ArticleOut(**a) for a in articles]


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


def load_articles_by_tag(tag: str) -> list[ArticleOut]:
    articles = load_articles()

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


# Users
def create_user(user: UserIn):
    hashed_password = get_password_hash(user.password)
    user_db = UserDb(**user.model_dump(), hashed_password=hashed_password)
    db["Users"].append(user_db.model_dump())
    save_db(db, DB_PATH)


def get_user(username):
    users = db["Users"]
    for u in users:
        if u["username"] == username:
            return u
    return None


# Security
load_dotenv()

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    user_dict = get_user(username)
    if not user_dict:
        verify_password(password, DUMMY_HASH)
        return False

    user = UserDb(**user_dict)

    # Most hash it!
    if not verify_password(password, user.hashed_password):
        return False

    return user


# Token

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt
