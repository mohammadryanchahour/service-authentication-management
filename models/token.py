from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

from helpers.enums import TokenType


class Token(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    token: str
    token_type: TokenType
    user_id: str
    expires_at: datetime
    created_at: datetime.now
    is_active: bool = True 