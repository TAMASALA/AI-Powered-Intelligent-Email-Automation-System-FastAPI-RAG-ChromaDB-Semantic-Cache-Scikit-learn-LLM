import re
import string
import pandas as pd
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# ==========================================================
# Download NLTK Resources
# ==========================================================

try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))

try:
    lemmatizer = WordNetLemmatizer()
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")
    nltk.download("omw-1.4")
    lemmatizer = WordNetLemmatizer()


# ==========================================================
# Text Preprocessing
# ==========================================================

def preprocess_text(text: str) -> str:
    """
    Preprocess email text before prediction.
    """

    if text is None or pd.isna(text):
        return ""

    text = str(text).lower()

    # Remove HTML
    text = re.sub(r"<.*?>", " ", text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Remove Email IDs
    text = re.sub(r"\S+@\S+", " ", text)

    # Remove Numbers
    text = re.sub(r"\d+", " ", text)

    # Remove Punctuation
    text = text.translate(
        str.maketrans(
            "",
            "",
            string.punctuation
        )
    )

    # Remove Extra Spaces
    text = re.sub(r"\s+", " ", text).strip()

    words = []

    for word in text.split():

        if word not in stop_words:

            words.append(
                lemmatizer.lemmatize(word)
            )

    return " ".join(words)