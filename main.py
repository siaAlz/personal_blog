import datetime
import json
import os

from fastapi import FastAPI

app = FastAPI()


# Creating DB
def initiate_db():
    seed: list = [
        {
            "id": 0,
            "author": "sia",
            "title": "Welcome",
            "content": "Hi this is my first app.",
            "created_at": "2026-06-09T19:22:03.614869",
        },
    ]

    os.makedirs("db", exist_ok=True)
    db_path = os.path.join(os.getcwd(), "db", "db.json")
    if not os.path.exists(os.path.join(db_path, "db.json")):
        with open(db_path, mode="w", encoding="utf-8") as file:
            json.dump(seed, file, indent="")

    return db_path


db = initiate_db()


@app.get("/")
async def home():
    return {"message": "Blog App"}


@app.get("/articles")
async def get_articles():

    with open(db, mode="r", encoding="utf-8") as file:
        articles = json.load(file)
        return articles

    # Returns All Articles
