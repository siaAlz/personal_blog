from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)


class UserIn(UserBase):
    password: str = Field(min_length=6, max_length=50)


class UserDb(UserBase):
    hashed_password: str = Field()


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    image_file: str | None
    image_path: str
    # Should we include email in user response?
