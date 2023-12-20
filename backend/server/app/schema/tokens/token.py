from pydantic import BaseModel


class BaseToken(BaseModel):
    token_type: str


class AccessToken(BaseToken):
    access_token: str
    created_at: str


class RefreshToken(BaseToken):
    refresh_token: str
    created_at: str


class TokenData(BaseModel):
    username: str | None = None
