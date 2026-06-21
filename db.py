import os
import json


def initiate_db():
    seed: dict[str, list[dict]] = {
        "Articles": [
            {
                "id": 1,
                "author": "sia",
                "title": "Welcome",
                "content": "Hi this is my first app.",
                "created_at": "2026-06-09T19:22:03.614869",
            },
        ],
        "Users": [{"username": "siavash", "password": "siavash", "is_active": False}],
    }

    os.makedirs("db", exist_ok=True)
    db_path = os.path.join("db", "db.json")
    if not os.path.exists(db_path):
        with open(db_path, mode="w", encoding="utf-8") as db:
            json.dump(seed, db, indent=4)

    return db_path


def load_db(db_path) -> dict[str, list[dict]]:
    with open(db_path, mode="r", encoding="utf-8") as db:
        data = json.load(db)
    return data


def save_db(data, db_path):
    with open(db_path, mode="w", encoding="utf-8") as db:
        json.dump(data, db, indent=4)
