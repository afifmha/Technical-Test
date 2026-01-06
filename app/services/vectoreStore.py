from app.core.interfaces import VectorStoreInterface
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from app.core.config import settings

class QdrantVectorStore(VectorStoreInterface):
    def __init__(self):
        self.client = QdrantClient(url=str(settings.QDRANT_URL)) 
        self.collection_name = settings.QDRANT_COLLECTION
        if not self.client.collection_exists(self.collection_name):
            print(f"Collection {self.collection_name} not found. Creating...")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=128, distance=Distance.COSINE)
            )
        else:
            print(f"Connected to existing collection: {self.collection_name}")

    def add_documents(self, text: str, vector: list[float]):
        doc_id = abs(hash(text)) % 1000000 
        self.client.upsert(
            collection_name=self.collection_name,
            points=[PointStruct(id=doc_id, vector=vector, payload={"text": text})]
        )

    def search(self, query_vector: list[float], limit: int = 2) -> list[str]:
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=5
        )
        return [hit.payload["text"] for hit in search_result.points]
    
    def document_count(self) -> int:
        try:
            info = self.client.get_collection(self.collection_name)
            return info.points_count
        except Exception:
            return 0

class LocalVectorStore(VectorStoreInterface):
    def __init__(self):
        self.store = []

    def add_documents(self, text: str, vector: list[float]):
        self.store.append(text)

    def search(self, query_vector: list[float], limit: int = 2) -> list[str]:
        return self.store[:limit]
    
    def document_count(self) -> int:
        return len(self.store)