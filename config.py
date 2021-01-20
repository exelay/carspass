import os
from dotenv import load_dotenv

load_dotenv()

# Environment variables
PROXY_TOKEN = str(os.getenv("PROXY_TOKEN"))
