from app.rag.vector_store import get_vector_store

from app.config import TOP_K


def retrieve_context(

    query,

    top_k=TOP_K

):

    results = get_vector_store().search(

        query=query,

        top_k=top_k

    )

    documents = results.get(

        "documents",

        [[]]

    )[0]

    metadata = results.get(

        "metadatas",

        [[]]

    )[0]

    context = []

    for doc, meta in zip(

        documents,

        metadata

    ):

        source = meta.get(

            "source",

            "Unknown"

        )

        context.append(

            f"[Source: {source}]\n{doc}"

        )

    return "\n\n".join(context)


if __name__ == "__main__":

    query = input("Query : ")

    response = retrieve_context(query)

    print("\n")

    print("=" * 60)

    print(response)