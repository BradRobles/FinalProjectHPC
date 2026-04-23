import os
from dotenv import load_dotenv

def setup_project():
    load_dotenv()

    os.makedirs("results", exist_ok=True)

    api_key = os.getenv("MAP_KEY")

    if not api_key:
        raise ValueError("MAP_KEY no encontrada")

    return api_key