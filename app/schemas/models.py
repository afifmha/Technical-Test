from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str

class DocumentRequest(BaseModel):
    text: str

class QuestionResponse(BaseModel):
    question: str
    answer: str
    context_used: list[str]
    latency_sec: float