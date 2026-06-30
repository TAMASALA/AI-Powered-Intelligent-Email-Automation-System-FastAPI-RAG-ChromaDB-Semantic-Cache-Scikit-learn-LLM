import chromadb
import uuid
import os

from chromadb.config import Settings
from app.config import (
    CHROMA_DB,
    SEMANTIC_CACHE_COLLECTION,
    CACHE_THRESHOLD
)

from app.rag.embedding import embed_text


class SemanticCache:

    def __init__(self):

        os.makedirs(CHROMA_DB, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DB),
            settings=Settings(anonymized_telemetry=False)
        )

        self.collection = self.client.get_or_create_collection(
            name=SEMANTIC_CACHE_COLLECTION,
            metadata={"hnsw:space": "cosine"}
        )

    # =========================
    # EMBEDDING
    # =========================
    def _embed(self, text: str):
        return embed_text(text.strip().lower())

    # =========================
    # SEARCH
    # =========================
    def search(self, email: str):

        if self.collection.count() == 0:
            return None

        query_embedding = self._embed(email)

        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )

        if not result.get("documents") or not result["documents"][0]:
            return None

        distance = result["distances"][0][0]

        similarity = max(0.0, 1 - float(distance))

        print(f"[CACHE DEBUG] similarity = {similarity}")

        if similarity >= CACHE_THRESHOLD:
            return {
                "response": result["metadatas"][0][0]["response"],
                "similarity": similarity
            }

        return None

    # =========================
    # ADD
    # =========================
    def add(self, email: str, response: str):

        embedding = self._embed(email)

        uid = str(uuid.uuid4())

        self.collection.add(
            ids=[uid],
            embeddings=[embedding],
            documents=[email],
            metadatas=[{"response": response}]
        )

    def count(self):
        return self.collection.count()


# =========================
# SINGLETON
# =========================
_semantic_cache = None

def get_semantic_cache():
    global _semantic_cache
    if _semantic_cache is None:
        _semantic_cache = SemanticCache()
    return _semantic_cache


def search_cache(email: str):
    cache = get_semantic_cache()
    result = cache.search(email)
    return result["response"] if result else None


def save_cache(email: str, response: str):
    get_semantic_cache().add(email, response)