"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    echo=settings.debug
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency for getting database sessions
    
    Usage:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables
    
    Call this function to create all tables defined in models
    """
    from app import models  # Import here to avoid circular imports
    Base.metadata.create_all(bind=engine)


def drop_db():
    """
    Drop all database tables
    
    WARNING: This will delete all data!
    Use only for testing or development
    """
    from app import models  # Import here to avoid circular imports
    Base.metadata.drop_all(bind=engine)

# Made with Bob
