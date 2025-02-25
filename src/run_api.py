import uvicorn
import os
import logging
from api.main import app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Run the API server"""
    try:
        host = os.getenv('API_HOST', '0.0.0.0')
        port = int(os.getenv('API_PORT', '8000'))
        
        logger.info(f"Starting API server on {host}:{port}")
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info"
        )
        
    except Exception as e:
        logger.error(f"Error starting API server: {str(e)}")
        raise

if __name__ == "__main__":
    main() 