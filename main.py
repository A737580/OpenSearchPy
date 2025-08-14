import uvicorn
from faker import Faker
from fastapi import FastAPI
import random
from core.opensearch_client import create_index, index_documents, search_documents, settings
from fastapi.responses import RedirectResponse
from typing import Optional
from core.models import ContentType

app = FastAPI()

fake = Faker()

@app.on_event("startup")
async def startup_event():
    create_index()

@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.post("/load_data")
def load_data():
    content_types = list(ContentType)
    documents = []
    for _ in range(5):
        doc = {
            "title": fake.catch_phrase(),  
            "content": fake.text(max_nb_chars=200), 
            "content_type": random.choice(content_types).value
        }
        documents.append(doc)
    
    index_documents(documents)
    return {"message": "Random documents loaded successfully."}

@app.get("/search")
def search(query: Optional[str] = None, content_type: Optional[ContentType] = None):

    results = search_documents(query, content_type)
    return {"results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)