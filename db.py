import os
import json


def initiate_db():
    seed: list = [
        {
            "id": 1,
            "author": "sia",
            "title": "Welcome",
            "content": "Hi this is my first app.",
            "created_at": "2026-06-09T19:22:03.614869",
        },
    ]

    os.makedirs("db", exist_ok=True)
    db_path = os.path.join("db", "db.json")
    if not os.path.exists(db_path):
        with open(db_path, mode="w", encoding="utf-8") as db:
            json.dump(seed, db, indent="")

    return db_path
