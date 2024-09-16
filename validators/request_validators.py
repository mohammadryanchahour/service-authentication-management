from typing import Optional
from pydantic import BaseModel

from helpers.enums import TokenType

class LoginRequest(BaseModel):
    email: Optional[str] = ""
    username: Optional[str] = ""
    password: str = ""

class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str
    confirm_password: str
    reset_token: str

class LogoutRequest(BaseModel):
    token: str

class TokenRequest(BaseModel):
    user_id: str = ""

