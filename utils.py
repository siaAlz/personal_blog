import json

from models import ArticleBase, ArticleModel
from db import initiate_db

# DB
DB_PATH = initiate_db()


def load_articles() -> list[ArticleModel]:
    with open(DB_PATH, mode="r", encoding="utf-8") as file:
        articles = json.load(file)

    return [ArticleModel(**a) for a in articles]


def load_article(article_id: int) -> ArticleModel | None:
    articles = load_articles()
    for a in articles:
        if a.id == article_id:
            return a


def create_article(article: ArticleModel):
    articles = load_articles()
    articles.sort(key=lambda article: article.id)
    last_id = articles[-1].id

    new_article = ArticleModel(
        **article.model_dump(),
        id=last_id + 1,
    )

    articles.append(new_article)
    with open(DB_PATH, mode="w", encoding="utf-8") as db:
        json.dump([a.model_dump() for a in articles], db)

    return new_article


def load_articles_by_tag(tag: str) -> list[ArticleModel]:
    articles = load_articles()

    articles_by_tag = [a for a in articles if tag in a.tags]
    return articles_by_tag


def upload_article(article_id: int, updated_article: ArticleBase) -> ArticleBase | None:
    articles = load_articles()

    for i, article in enumerate(articles):
        if article.id == article_id:
            articles[i] = ArticleModel(
                **updated_article.model_dump(),
                id=articles[i].id,
                created_at=articles[i].created_at,
            )

            with open(DB_PATH, mode="w", encoding="utf-8") as db:
                json.dump(
                    [a.model_dump() for a in articles],
                    db,
                    indent=4,
                )

            return updated_article
    return None
