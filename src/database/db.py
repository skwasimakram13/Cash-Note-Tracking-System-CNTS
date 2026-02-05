from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import Config
from src.database.models import Base
import os

# Ensure data directory exists
os.makedirs(Config.DATA_DIR, exist_ok=True)

engine = create_engine(Config.DB_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
