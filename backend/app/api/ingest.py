from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ingest import ingest_pdf

router = APIRouter(prefix="/api", tags=["ingest"])

class IngestRequest(BaseModel):
    url: str
    source_name: str = "履修要綱.pdf"

class IngestResponse(BaseModel):
    message: str
    chunk_count: int

@router.post("/ingest", response_model=IngestResponse)
def ingest(body: IngestRequest):
    try:
        n = ingest_pdf(url=body.url, source_name=body.source_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return IngestResponse(message="取り込み完了", chunk_count=n)