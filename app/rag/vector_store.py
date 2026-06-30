import chromadb

from chromadb.config import Settings

from app.config import (
    CHROMA_DB,
    CHROMA_COLLECTION
)

from app.rag.embedding import get_embedding_model, embed_text
from app.rag.knowledge_loader import KnowledgeLoader


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DB),
            settings=Settings(
                anonymized_telemetry=False
            )
        )

        self.collection = self.client.get_or_create_collection(
            name=CHROMA_COLLECTION,
            metadata={"hnsw:space": "cosine"}
        )

    # ======================================

    def index_documents(self):

        loader = KnowledgeLoader()

        documents = loader.load_documents()

        if len(documents) == 0:

            print("No Knowledge Documents Found.")

            return

        print(f"Indexing {len(documents)} Chunks...")

        for index, doc in enumerate(documents):

            embedding = embed_text(doc["content"])

            self.collection.add(

                ids=[str(index)],

                embeddings=[embedding],

                documents=[doc["content"]],

                metadatas=[

                    {

                        "source": doc["source"]

                    }

                ]

            )

        print("Knowledge Base Indexed Successfully.")

    # ======================================

    def search(

        self,

        query,

        top_k=5

    ):

        query_embedding = embed_text(query)

        results = self.collection.query(

            query_embeddings=[query_embedding],

            n_results=top_k

        )

        return results

    # ======================================

    def total_documents(self):

        return self.collection.count()


# Lazy loading of vector store
_vector_store = None

def get_vector_store():
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store

vector_store = None  # Will be loaded lazily


if __name__ == "__main__":

    get_vector_store().index_documents()

    print(get_vector_store().total_documents())