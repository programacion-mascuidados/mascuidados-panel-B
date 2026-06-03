from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class LoginResponse(BaseModel):
    message: str
    username: str
    role: str
    allowed_panels: list[str]


class AuthStatusResponse(BaseModel):
    authenticated: bool
    username: str | None = None
    role: str | None = None
    allowed_panels: list[str] = []
