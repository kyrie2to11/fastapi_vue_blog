from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class About(Base):
    __tablename__ = "about"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<About Page>"