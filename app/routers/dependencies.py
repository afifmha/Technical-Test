from fastapi import Depends
from app.core.interfaces import VectorStoreInterface as VectorStore
from app.services.vectoreStore import QdrantVectorStore,LocalVectorStore
from app.services.ragServices import RAGService

def getVectorStore() -> VectorStore:
    try:
        return QdrantVectorStore() 
    except Exception:
        return LocalVectorStore()

def getRagServices(store: VectorStore = Depends(getVectorStore)) -> RAGService:
    return RAGService(store)