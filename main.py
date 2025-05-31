from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.retrieval import LegalRetrieval
import uvicorn

app = FastAPI(
    title="Legal Document Search API",
    description="API for searching legal documents using PhoBERT embeddings and FAISS",
    version="1.0.0"
)

retriever = None

class SearchQuery(BaseModel):
    query: str
    k: Optional[int] = 5

class SearchResult(BaseModel):
    id: str
    title: str
    text: str
    file: str
    score: float

class SearchResponse(BaseModel):
    results: List[SearchResult]

@app.on_event("startup")
def startup_event():
    # Initialize the retriever
    global retriever
    retriever = LegalRetrieval()
    json_dir = "articles_parsing"
    retriever.build_embeddings(json_dir)

@app.post("/search", response_model=SearchResponse)
async def search(query: SearchQuery):
    if retriever is None:
        raise HTTPException(status_code=500, detail="Retriever not initialized")
    
    try:
        results = retriever.search(query=query.query, k=query.k)
        return SearchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 