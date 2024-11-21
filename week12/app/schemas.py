from typing import List, Union

from pydantic import BaseModel


class PasteBase(BaseModel):
    title: str


class PasteCreate(PasteBase):
    content: str


class Paste(PasteBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    pastes: List[Paste] = []

    class Config:
        from_attributes = True

class UserDetail(User):
    salt: str
