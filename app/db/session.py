from sqlalchemy import create_engine 
from app.core.config import settings 
from app.db.base import Base

from sqlalchemy.orm import Session  , sessionmaker
from collections.abc import Generator



engine = create_engine(
    settings.database_url
)

def create_tables():
    Base.metadata.create_all(bind = engine)
    
SessionLocal = sessionmaker(
    bind=engine , 
    autoflush=False  , 
    autocommit = False
)
    
def get_session() -> Generator[Session , None  , None] : 
    
    db = SessionLocal()
    
    try: 
        yield db
    finally: 
        db.close()