from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ml.predictor import predict_email
from app.cache.semantic_cache import search_cache, save_cache
from app.rag.retriever import retrieve_context
from app.llm.response_generator import generate_response
from app.logger.conversation_logger import save_conversation


# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    prefix="/api/v1",
    tags=["Email Automation"]
)


# ==========================================================
# Request Schema
# ==========================================================

class EmailRequest(BaseModel):
    email: str


# ==========================================================
# Response Schema
# ==========================================================

class EmailResponse(BaseModel):
    classification: str
    cache_status: str
    similarity_score: float
    rag_context: str
    response: str
    source: str


# ==========================================================
# MAIN PIPELINE
# ==========================================================

@router.post("/process-email", response_model=EmailResponse)
async def process_email(request: EmailRequest):

    try:
        email_text = (request.email or "").strip()

        if not email_text:
            raise HTTPException(
                status_code=400,
                detail="Email cannot be empty."
            )

        print("\n========== PIPELINE START ==========")

        # ==================================================
        # STEP 1: SEMANTIC CACHE
        # ==================================================
        print("Step 1: Semantic Cache Check")

        cache_result = search_cache(email_text)

        if cache_result:

            print("Cache HIT")

            save_conversation(
                email=email_text,
                classification="HAM",
                context="CACHE",
                response=cache_result,
                source="Semantic Cache"
            )

            return EmailResponse(
                classification="HAM",
                cache_status="HIT",
                similarity_score=1.0,
                rag_context="CACHE",
                response=cache_result,
                source="Semantic Cache"
            )

        print("Cache MISS")

        # ==================================================
        # STEP 2: SPAM DETECTION
        # ==================================================
        print("Step 2: Spam Detection")

        prediction = predict_email(email_text)

        if prediction == "SPAM":

            print("Spam Detected")

            save_conversation(
                email=email_text,
                classification="SPAM",
                context="",
                response="Spam email blocked.",
                source="ML Model"
            )

            return EmailResponse(
                classification="SPAM",
                cache_status="MISS",
                similarity_score=0.0,
                rag_context="",
                response="Spam email blocked.",
                source="ML Model"
            )

        # ==================================================
        # STEP 3: RAG RETRIEVAL
        # ==================================================
        print("Step 3: RAG Retrieval")

        context = retrieve_context(email_text)

        # safe fallback
        if context is None:
            context = ""

        # ==================================================
        # STEP 4: LLM RESPONSE
        # ==================================================
        print("Step 4: LLM Generation")

        reply = generate_response(
            email=email_text,
            context=context
        )

        # ==================================================
        # STEP 5: SAVE CACHE + LOG
        # ==================================================
        print("Step 5: Save Cache")

        save_cache(email_text, reply)

        save_conversation(
            email=email_text,
            classification="HAM",
            context=context,
            response=reply,
            source="LLM"
        )

        print("========== PIPELINE END ==========\n")

        return EmailResponse(
            classification="HAM",
            cache_status="MISS",
            similarity_score=0.0,
            rag_context=context,
            response=reply,
            source="LLM"
        )

    except Exception as e:

        print("🔥 ERROR IN PIPELINE:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )