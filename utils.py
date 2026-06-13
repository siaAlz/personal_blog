import json

from datetime import datetime
from models import ArticleModel
from db import initiate_db

# DB
DB_PATH = initiate_db()


def load_articles():
    with open(DB_PATH, mode="r", encoding="utf-8") as file:
        articles = json.load(file)
    return articles


def load_article(article_id):
    articles = load_articles()
    for a in articles:
        if a.get("id") == article_id:
            return a


def create_article(article: ArticleModel):
    articles: list = load_articles()
    articles.sort(key=lambda article: article["id"])
    last_id = articles[-1]["id"]

    new_article = {
        **article.model_dump(),
        "id": (last_id + 1),
        "created_at": datetime.now().isoformat(),
    }

    articles.append(new_article)
    with open(DB_PATH, mode="w", encoding="utf-8") as db:
        json.dump(articles, db)

    return new_article
