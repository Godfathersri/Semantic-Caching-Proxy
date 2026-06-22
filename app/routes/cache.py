from fastapi import APIRouter

from app.config import settings
from app.services.cache_service import (
    get_total_cache_items,
    get_collection_info
)
from app.services.vector_store import (
    vectorstore
)

router = APIRouter(
    prefix="/cache",
    tags=["Cache"]
)


@router.get("/stats")
async def cache_stats():

    collection_info = (
        get_collection_info()
    )

    return {
        "collection_name":
            settings.QDRANT_COLLECTION,

        "total_cached_items":
            get_total_cache_items(),

        "embedding_model":
            settings.Embedding_Model,

        "embedding_dimension":
            settings.EMBEDDING_DIMENSION,

        "similarity_threshold":
            settings.QDRANT_SIMILARITY_THRESHOLD,

        "qdrant_status":
            "connected",

        "points_count":
            collection_info.points_count
    }


@router.get("/items")
async def cache_items():

    items = (
        vectorstore.get_recent_items(
            limit=10
        )
    )

    return {
        "count": len(items),

        "items": [
            {
                "id": str(item.id),

                "prompt":
                    item.payload.get(
                        "prompt"
                    ),

                "cache_status":
                    item.payload.get(
                        "cache_status"
                    ),

                "cache_hits":
                    item.payload.get(
                        "cache_hits"
                    ),

                "created_at":
                    item.payload.get(
                        "created_at"
                    ),

                "last_accessed_at":
                    item.payload.get(
                        "last_accessed_at"
                    )
            }

            for item in items
        ]
    }