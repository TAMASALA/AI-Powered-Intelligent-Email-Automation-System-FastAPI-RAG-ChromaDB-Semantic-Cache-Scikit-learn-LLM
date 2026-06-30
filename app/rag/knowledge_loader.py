import os

from pathlib import Path

try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False
    PdfReader = None

from app.config import KNOWLEDGE_BASE

from app.rag.chunking import TextChunker


class KnowledgeLoader:

    def __init__(self):
        if not HAS_PYPDF:
            raise RuntimeError(
                "pypdf is not installed. "
                "Install it with: pip install pypdf"
            )
        self.chunker = TextChunker()

    def read_pdf(self, file_path):

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:

                text += extracted + "\n"

        return text

    def read_text(self, file_path):

        with open(

            file_path,

            "r",

            encoding="utf-8"

        ) as f:

            return f.read()

    def load_documents(self):

        documents = []

        directory = Path(KNOWLEDGE_BASE)

        for file in directory.iterdir():

            if file.suffix.lower() == ".pdf":

                text = self.read_pdf(file)

            elif file.suffix.lower() == ".txt":

                text = self.read_text(file)

            else:

                continue

            chunks = self.chunker.split(text)

            for chunk in chunks:

                documents.append({

                    "content": chunk,

                    "source": file.name

                })

        return documents


if __name__ == "__main__":

    loader = KnowledgeLoader()

    docs = loader.load_documents()

    print("Chunks :", len(docs))