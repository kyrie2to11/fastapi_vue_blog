from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.article import Article
from app.schemas.article import ArticleRead  # Correct import of ArticleRead
from app.schemas.home import HomeResponse

router = APIRouter(
    prefix="/api/v1/home",
    tags=["home"]
)

@router.get("/", response_model=HomeResponse)
def get_home_data(db: Session = Depends(get_db)):
    """获取首页数据，包括最新文章、特色内容等"""
    try:
        # 获取最新5篇文章
        recent_articles = db.query(Article).order_by(Article.created_at.desc()).limit(5).all()
        
        # 可添加其他首页数据（如热门文章、分类统计等）
        featured_content = {
            "banner": "https://example.com/banner.jpg",
            "site_intro": "个人博客首页，记录学习心得与日常分享"
        }

        return HomeResponse(
            recent_articles=[ArticleRead.from_orm(article) for article in recent_articles],
            featured_content=featured_content
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取首页数据失败: {str(e)}")