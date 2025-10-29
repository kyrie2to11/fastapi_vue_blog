from typing import Any, Dict, List, Optional, Union
from pydantic import BaseSettings, validator
from pydantic.networks import AnyUrl
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SERVER_NAME: str = "FastAPI Blog"
    SERVER_HOST: str = "localhost"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:3000", "http://localhost:8000"]
    
    # Database
    DATABASE_URI: Optional[AnyUrl] = None
    
    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        # Construct URI manually to avoid AnyUrl.build parameter errors
        user = values.get("POSTGRES_USER")
        password = values.get("POSTGRES_PASSWORD")
        host = values.get("POSTGRES_SERVER")
        db_name = values.get("POSTGRES_DB") or ""
        if user and password and host:
            return f"postgresql://{user}:{password}@{host}/{db_name}"
        return v  # Fallback to existing value if any part is missing

    class Config:
        case_sensitive = True
        env_file = ".env"

    # OAuth Providers (use Optional to handle missing env vars)
    GITHUB_CLIENT_ID: Optional[str] = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET: Optional[str] = os.getenv("GITHUB_CLIENT_SECRET")
    GITHUB_REDIRECT_URI: str = os.getenv("GITHUB_REDIRECT_URI", f"{SERVER_HOST}/api/v1/auth/callback/github")

    WECHAT_CLIENT_ID: Optional[str] = os.getenv("WECHAT_CLIENT_ID")
    WECHAT_CLIENT_SECRET: Optional[str] = os.getenv("WECHAT_CLIENT_SECRET")
    WECHAT_REDIRECT_URI: str = os.getenv("WECHAT_REDIRECT_URI", f"{SERVER_HOST}/api/v1/auth/callback/wechat")

    QQ_CLIENT_ID: Optional[str] = os.getenv("QQ_CLIENT_ID")
    QQ_CLIENT_SECRET: Optional[str] = os.getenv("QQ_CLIENT_SECRET")
    QQ_REDIRECT_URI: str = os.getenv("QQ_REDIRECT_URI", f"{SERVER_HOST}/api/v1/auth/callback/qq")

settings = Settings()