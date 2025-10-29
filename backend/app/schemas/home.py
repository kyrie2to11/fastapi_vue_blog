from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.article import ArticleRead  # Fixed: Import ArticleRead instead of Article

class HomeResponse(BaseModel):
    recent_articles: List[ArticleRead]  # Fixed: Use ArticleRead instead of Article
    featured_content: dict  # Contains banner, site_intro, etc.