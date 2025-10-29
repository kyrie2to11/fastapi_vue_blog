from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    sender_id: int
    content: str

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: int
    created_at: datetime
    is_read: bool

    class Config:
        orm_mode = True