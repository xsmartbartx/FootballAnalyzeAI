from pathlib import Path
import os
from database.config import DatabaseConfig
from database.connection import DatabaseConnection

def main():
    # Load database configuration from environment variables
    config = DatabaseConfig(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', '5432')),
        database=os.getenv('DB_NAME', 'football_tracking'),
        username=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', '')
    )
    
    # Initialize database connection
    db = DatabaseConnection(config)
    
    # Create database tables
    print("Creating database tables...")
    db.create_database()
    print("Database initialization completed!")

if __name__ == "__main__":
    main() 