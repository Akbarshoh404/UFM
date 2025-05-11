import os
from dotenv import load_dotenv

load_dotenv()

# Configuration settings
DATABASE_URL = os.environ.get("DATABASE_URL")