from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.config import EMBEDDING_MODEL


class Similarity:

    def __init__(self):

        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    def embedding(self, text):

        return self.model.encode(
            text,
            normalize_embeddings=True
        )

    def score(self, text1, text2):

        emb1 = self.embedding(text1)

        emb2 = self.embedding(text2)

        similarity = cosine_similarity(
            [emb1],
            [emb2]
        )[0][0]

        return float(similarity)


similarity_engine = Similarity()


if __name__ == "__main__":

    text1 = "I need sick leave tomorrow."

    text2 = "Can I apply for sick leave?"

    print(

        similarity_engine.score(
            text1,
            text2
        )

    )