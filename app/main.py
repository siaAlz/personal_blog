from fastapi import FastAPI
from app.routers import articles, users, auth

app = FastAPI()

app.include_router(articles.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/", tags=["public"])
async def home():
    """
    This the home description. just for test!
    """
    return {"message": "Hi 🫠"}
