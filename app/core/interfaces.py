from abc import ABC, abstractmethod

class VectorStoreInterface(ABC):
    @abstractmethod
    def add_documents(self, documents: list[str]) -> None:
        """Add documents to the vector store."""
        raise NotImplementedError
    
    @abstractmethod
    def search(self, question: str, limit: int = 5) -> list[str]:
        """Query the vector store for similiar/relevant documents."""
        raise NotImplementedError
    
    @abstractmethod
    def document_count(self) -> int:
        """Return the number of documents in the vector store."""
        raise NotImplementedError