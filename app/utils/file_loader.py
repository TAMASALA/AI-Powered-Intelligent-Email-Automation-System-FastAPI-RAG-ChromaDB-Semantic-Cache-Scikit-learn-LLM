from pathlib import Path

from pypdf import PdfReader


# =============================================
# Read TXT File
# =============================================

def load_text(file_path):

    with open(

        file_path,

        "r",

        encoding="utf-8"

    ) as file:

        return file.read()


# =============================================
# Read PDF File
# =============================================

def load_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:

            text += extracted + "\n"

    return text


# =============================================
# Load Any File
# =============================================

def load_file(file_path):

    file_path = Path(file_path)

    suffix = file_path.suffix.lower()

    if suffix == ".txt":

        return load_text(file_path)

    elif suffix == ".pdf":

        return load_pdf(file_path)

    else:

        raise ValueError(

            f"Unsupported File : {suffix}"

        )


# =============================================
# Load Directory
# =============================================

def load_directory(directory):

    documents = []

    directory = Path(directory)

    for file in directory.iterdir():

        if file.suffix.lower() in [

            ".pdf",

            ".txt"

        ]:

            documents.append(

                {

                    "name": file.name,

                    "content": load_file(file)

                }

            )

    return documents


if __name__ == "__main__":

    docs = load_directory(

        "knowledge_base"

    )

    print(

        f"Loaded {len(docs)} documents."

    )