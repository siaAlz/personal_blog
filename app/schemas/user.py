from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    is_active: bool = True


class UserIn(UserBase):
    password: str = Field(min_length=6, max_length=50)


class UserDb(UserBase):
    hashed_password: str = Field()
