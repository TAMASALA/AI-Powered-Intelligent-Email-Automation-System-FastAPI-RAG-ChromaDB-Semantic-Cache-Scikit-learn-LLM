import joblib
import logging
from functools import lru_cache

from app.config import MODEL_PATH, VECTORIZER_PATH
from app.ml.preprocess import preprocess_text

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def load_artifacts():
    try:
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)

        logger.info("Spam model loaded successfully.")
        return model, vectorizer

    except Exception as e:
        logger.error(f"Model Loading Failed: {e}")
        raise RuntimeError(f"Unable to load ML model: {e}")


def predict_email(email: str) -> str:

    model, vectorizer = load_artifacts()

    cleaned = preprocess_text(email)

    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)[0]

    return "SPAM" if prediction == 1 else "HAM"


def predict_probability(email: str):

    model, vectorizer = load_artifacts()

    cleaned = preprocess_text(email)

    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)[0]

    confidence = None

    if hasattr(model, "predict_proba"):
        confidence = float(max(model.predict_proba(vector)[0]))

    return {
        "prediction": "SPAM" if prediction == 1 else "HAM",
        "confidence": confidence
    }