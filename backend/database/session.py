from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import User
from models.photo import Photo

DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/photo_db"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()