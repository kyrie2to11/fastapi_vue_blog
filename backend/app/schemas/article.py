from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ArticleBase(BaseModel):
    title: str
    slug: str
    content: str
    summary: Optional[str] = None
    category_id: Optional[int] = None
    is_published: bool = False

class ArticleCreate(ArticleBase):
    pass

class ArticleRead(ArticleBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    view_count: int

    class Config:
        orm_mode = True

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    category_id: Optional[int] = None
    is_published: Optional[bool] = None