from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    bio: Optional[str] = Field(None)
    profile_image: Optional[str] = Field(None)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None)
    profile_image: Optional[str] = Field(None)

class UserInDBBase(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

class User(UserInDBBase):
    class Config:
        orm_mode = True

class UserInDB(UserInDBBase):
    hashed_password: str
    provider: Optional[str] = None
    provider_id: Optional[str] = None