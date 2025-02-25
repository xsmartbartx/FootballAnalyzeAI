from dataclasses import dataclass
from typing import Optional

@dataclass
class DatabaseConfig:
    """Database configuration"""
    host: str
    port: int
    database: str
    username: str
    password: str
    
    @property
    def connection_string(self) -> str:
        """Get SQLAlchemy connection string"""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}" 