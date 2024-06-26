from pydantic import BaseModel
from typing import List

class UserBlog(BaseModel):
    id : int
    title : str

class UserBase(BaseModel):
    username : str
    name : str

class UserCreate(UserBase):
    password : str

class UserRead(UserBase):
    id : int
    user_blogs : List[UserBlog] = []
    class Config:
        from_attributes = True

class BlogBase(BaseModel):
    title : str
    body : str | None = None

class BlogCreate(BlogBase):
    pass

class BlogRead(BlogBase):
    user : int
    id : int
    class Config:
        from_attributes = True

class BlogEdit(BlogBase):
    title : str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None