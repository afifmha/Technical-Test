import time
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.models import QuestionRequest, DocumentRequest, QuestionResponse
from app.services.ragServices import RAGService
from app.routers.dependencies import getRagServices

router = APIRouter()

@router.post("/ask", response_model=QuestionResponse)
def ask_question(
    req: QuestionRequest, 
    service: RAGService = Depends(getRagServices)
):
    start = time.time()
    try:
        result = service.process_question(req.question)
        return {
            "question": req.question,
            "answer": result["answer"],
            "context_used": result.get("context", []),
            "latency_sec": round(time.time() - start, 3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add")
def add_document(
    req: DocumentRequest, 
    service: RAGService = Depends(getRagServices)
):
    start = time.time()
    try:
        service.add_document(req.text)
        return {"status": "added",
                "text_preview": req.text[:20],
                "latency_sec": round(time.time() - start, 3)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))