import os
from dotenv import load_dotenv
load_dotenv()

class Api:
    url: str = os.getenv("BACKEND_URL", "http://localhost:8000/")