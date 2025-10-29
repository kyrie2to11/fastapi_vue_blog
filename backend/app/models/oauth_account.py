from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, nullable=False)  # e.g., "github", "wechat", "qq"
    provider_id = Column(String, nullable=False)  # Unique ID from the OAuth provider
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship to the user
    user = relationship("User", back_populates="oauth_accounts")