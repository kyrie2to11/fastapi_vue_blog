from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = 3600  # 1 hour default

class TokenPayload(BaseModel):
    sub: int  # User ID
    exp: int  # Expiration timestamp