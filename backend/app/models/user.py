from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import List, Optional
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    # 移除列定义上的类型注解，仅保留SQLAlchemy类型参数
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    profile_image = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # OAuth字段
    provider = Column(String, nullable=True)  # e.g., "github", "wechat", "qq"
    provider_id = Column(String, nullable=True)
    
    # 使用字符串字面量解决关系引用问题
    articles = relationship("Article", back_populates="author")
    messages = relationship("Message", back_populates="sender")