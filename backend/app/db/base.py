from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base  # 替换为SQLAlchemy 2.0+推荐的orm模块导入

Base = declarative_base()