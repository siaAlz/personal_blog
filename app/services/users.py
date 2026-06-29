from app.core.security import DUMMY_HASH, get_password_hash, verify_password
from app.db.db import initiate_db, save_db, load_db
from app.schemas.user import UserDb, UserIn

DB_PATH = initiate_db()
db = load_db(DB_PATH)


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
