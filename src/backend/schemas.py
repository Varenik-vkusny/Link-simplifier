from pydantic import BaseModel, ConfigDict, computed_field
from typing import Optional
from datetime import datetime
from .config import get_settings

settings = get_settings()


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
    short_code: str
    created_at: Optional[datetime] = None
    owner: UserOut
    click_count: int

    @computed_field
    @property
    def short_link(self) -> str:

        return f'{settings.base_url}{self.short_code}'

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    username: Optional[str] = None