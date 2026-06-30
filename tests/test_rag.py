from app.rag.retriever import retrieve_context

from app.rag.vector_store import vector_store


def test_vector_database():

    assert vector_store.total_documents() >= 0


def test_retriever():

    query = """

    Sick Leave Policy

    """

    context = retrieve_context(

        query

    )

    assert isinstance(

        context,

        str

    )


def test_search():

    result = vector_store.search(

        query="Meeting",

        top_k=3

    )

    assert "documents" in result