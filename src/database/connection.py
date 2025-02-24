from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from .config import DatabaseConfig
from .models import Base

class DatabaseConnection:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def _create_engine(self) -> Engine:
        return create_engine(
            self.config.connection_string,
            pool_pre_ping=True
        )
    
    def create_database(self) -> None:
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Get database session"""
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close() 