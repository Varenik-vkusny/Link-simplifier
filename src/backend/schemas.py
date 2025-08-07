from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class LinkIn(BaseModel):
    original_link: str


class LinkOut(BaseModel):
    id: int
    original_link: str
    short_link: str
    created_at: date
    owner: UserOut

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    username: Optional[str] = None