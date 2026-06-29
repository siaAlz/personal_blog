from typing import Annotated

from fastapi import Depends, FastAPI
from app.routers import articles, users, auth
from app.dependencies import oauth2_scheme

app = FastAPI()

app.include_router(articles.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/", tags=["public"])
async def home(token: Annotated["str", Depends(oauth2_scheme)]):
    """
    This the home description. just for test!
    """
    return {"message": "Blog App", "token": token}
