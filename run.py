import os
import logging
from dotenv import load_dotenv

import uvicorn

# Load environment variables from .env file
load_dotenv()

# Configure logging to log into a file
logging.basicConfig(
    filename='./app.log',  # Log file name
    level=logging.INFO,  # Log level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s\n'
)

if __name__ == "__main__":
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 5001))
    uvicorn.run("app.main:app", host=host, port=port, reload=True)