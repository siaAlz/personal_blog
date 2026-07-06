from fastapi import FastAPI

from app.db.database import Base, engine
from app.routers import articles, users, auth

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(articles.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def home():
    """
    This the home description. just for test!
    """
    return {"message": "Hi 🫠"}
