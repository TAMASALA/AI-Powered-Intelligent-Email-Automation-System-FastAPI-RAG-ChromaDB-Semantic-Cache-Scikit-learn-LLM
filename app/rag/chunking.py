try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    HAS_LANGCHAIN_TEXT_SPLITTERS = True
except ImportError:
    # Fallback for older LangChain versions
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        HAS_LANGCHAIN_TEXT_SPLITTERS = True
    except ImportError:
        HAS_LANGCHAIN_TEXT_SPLITTERS = False
        RecursiveCharacterTextSplitter = None


class TextChunker:

    def __init__(

        self,

        chunk_size=500,

        chunk_overlap=100

    ):
        if not HAS_LANGCHAIN_TEXT_SPLITTERS:
            raise RuntimeError(
                "langchain_text_splitters is not installed. "
                "Install it with: pip install langchain-text-splitters"
            )

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=chunk_size,

            chunk_overlap=chunk_overlap,

            separators=[

                "\n\n",

                "\n",

                ".",

                " ",

                ""

            ]

        )

    def split(self, text: str):

        return self.splitter.split_text(text)