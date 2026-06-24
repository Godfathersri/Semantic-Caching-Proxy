from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)
from uuid import uuid4
from datetime import datetime
from app.config import settings
from app.exceptions import QdrantStorageError, QdrantSearchError
from app.logger import logger

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

            logger.info(
                f"Created collection: "
                f"{self.collection_name}"
            )

        else:

            logger.info(
                f"Collection already exists: "
                f"{self.collection_name}"
            )

    def store_cache_item(
        self,
        prompt: str,
        response: str,
        embedding: list[float],
        model: str,
        cache_status: str,
        temperature: float = 0.7
    ) -> None:

        try:

            now = datetime.utcnow().isoformat()

            point = PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload={
                    "prompt": prompt,
                    "response": response,
                    "model": model,
                    "temperature": temperature,
                    "cache_status": cache_status,
                    "created_at": now,
                    "last_accessed_at": now,
                    "cache_hits": 0
                }
            )

            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )

        except Exception as e:
            raise QdrantStorageError(
                f"Qdrant storage failed: {str(e)}"
            )

    def update_cache_hit(
        self,
        point_id: str,
        payload: dict
    ) -> None:

        try:

            updated_payload = {
                **payload,
                "cache_hits": payload.get(
                    "cache_hits",
                    0
                ) + 1,
                "cache_status": "HIT",
                "last_accessed_at":
                    datetime.utcnow().isoformat()
            }

            self.client.set_payload(
                collection_name=self.collection_name,
                payload=updated_payload,
                points=[point_id]
            )

        except Exception as e:
            raise QdrantStorageError(
                f"Failed to update cache hit: {str(e)}"
            )

    def search_similar(
        self,
        embedding: list[float],
        limit: int = 1
    ):
        try:
            results = self.client.query_points(
                collection_name=self.collection_name,
                query=embedding,
                limit=limit,
                with_payload=True
            )

            if not results.points:
                return None

            return results.points[0]
            
        except Exception as e:
            raise QdrantSearchError(
                f"Qdrant search failed: {str(e)}"
            )
    
    def get_total_cache_items(self) -> int:
        try:
            results = self.client.count(
                collection_name = self.collection_name,
                exact=True
            )
            return results.count
        
        except Exception as e:

            raise QdrantSearchError(
                f"Failed to count cache items: {str(e)}"
            )
    
    def get_collection_info(self):
        return self.client.get_collection(
            collection_name=self.collection_name
        )

    def get_recent_items(
        self,
        limit: int = 10
    ):
        try:
            results, _ = self.client.scroll(
                collection_name=self.collection_name,
                limit=limit,
                with_payload=True,
                with_vectors=False
            )

            return results
            
        except Exception as e:

            raise QdrantSearchError(
                f"Failed to get collection info: {str(e)}"
            )

vectorstore = VectorStore()