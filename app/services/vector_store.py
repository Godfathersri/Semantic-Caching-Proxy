from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)
from uuid import uuid4
from datetime import datetime

from app.config import settings



class VectorStore:

    def __init__(self):

        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )

        self.collection_name = (
            settings.QDRANT_COLLECTION
        )

    def create_collection_if_not_exists(
        self
    ) -> None:

        collections = (
            self.client.get_collections()
        )

        existing_collections = [
            collection.name
            for collection in collections.collections
        ]

        if (
            self.collection_name
            not in existing_collections
        ):

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_DIMENSION,
                    distance=Distance.COSINE
                )
            )

            print(
                f"Created collection: "
                f"{self.collection_name}"
            )

        else:

            print(
                f"Collection already exists: "
                f"{self.collection_name}"
            )

def store_cache_item(
    self,
    prompt: str,
    response: str,
    embedding: list[float],
    model: str,
    chache_status: str
) -> None:

    point = PointStruct(
        id=str(uuid4()),
        vector=embedding,
        payload={
            "prompt": prompt,
            "response": response,
            "model": model,
            "created_at": datetime.utcnow().isoformat(),
            "cache_hits": 0
        }
    )

    self.client.upsert(
        collection_name=self.collection_name,
        points=[point]
    )

vectorstore = VectorStore()