from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    username: Optional[str] = None