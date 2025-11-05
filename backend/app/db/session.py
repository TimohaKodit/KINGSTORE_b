from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
DATABASE_URL = "postgresql://postgres:EZhbxCbZmoxUHgdXhYWePBGCTQBjQUib@postgres.railway.internal:5432/railway"
# Настройка движка и сессии
engine = create_engine(
    DATABASE_URL,
    # **DO NOT** include connect_args={"check_same_thread": False} here!
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

