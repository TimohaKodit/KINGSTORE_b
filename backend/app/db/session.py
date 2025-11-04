from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
DATABASE_URL = "postgresql://${{PGUSER}}:${{POSTGRES_PASSWORD}}@${{RAILWAY_PRIVATE_DOMAIN}}:5432/${{PGDATABASE}}"
# Настройка движка и сессии
engine = create_engine(
    DATABASE_URL,
    # **DO NOT** include connect_args={"check_same_thread": False} here!
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
