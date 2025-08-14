import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENSEARCH_HOST: str = os.getenv("OPENSEARCH_HOST")
    OPENSEARCH_PORT: int = int(os.getenv("OPENSEARCH_PORT"))
    OPENSEARCH_USER: str = os.getenv("OPENSEARCH_USER")
    OPENSEARCH_PASSWORD: str = os.getenv("OPENSEARCH_PASSWORD")
    OPENSEARCH_INDEX_NAME: str = os.getenv("OPENSEARCH_INDEX_NAME")

settings = Settings()