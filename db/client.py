# db/client.py
import os
import dotenv
import weaviate
from weaviate.classes.init import Auth

dotenv.load_dotenv()

WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def connect():
    headers = {"X-OpenAI-Api-Key": OPENAI_API_KEY}
    if WEAVIATE_API_KEY:
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=WEAVIATE_URL,
            auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
            headers=headers,
        )
    else:
        client = weaviate.connect_to_local(headers=headers)
    return client
