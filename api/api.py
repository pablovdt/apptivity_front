import os
from dotenv import load_dotenv
load_dotenv()

class Api:
    # url: str = os.getenv("BACKEND_URL", "http://localhost:8000/")
    url: str = os.getenv("BACKEND_URL", "https://apptivity.up.railway.app/")
