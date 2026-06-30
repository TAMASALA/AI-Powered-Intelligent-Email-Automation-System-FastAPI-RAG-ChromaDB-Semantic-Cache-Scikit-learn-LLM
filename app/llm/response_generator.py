import logging

from app.llm.prompt import build_prompt

from app.llm.primary_llm import get_primary_llm

from app.llm.fallback_llm import get_fallback_llm

logger = logging.getLogger(__name__)


# =====================================================
# Generate Response
# =====================================================

def generate_response(

    email,

    context

):

    prompt = build_prompt(

        email,

        context

    )

    # ==========================================
    # Primary LLM
    # ==========================================

    try:

        logger.info("Using Primary LLM")

        response = get_primary_llm().generate(

            prompt

        )

        return response

    # ==========================================
    # Fallback
    # ==========================================

    except Exception:

        logger.warning(

            "Switching to Fallback LLM"

        )

        response = get_fallback_llm().generate(

            prompt

        )

        return response


# =====================================================
# Test
# =====================================================

if __name__ == "__main__":

    email = """

    Hi HR,

    I am suffering from fever.

    Kindly grant me one day sick leave.

    Regards,
    Vinay

    """

    context = """

    Sick leave can be approved
    after notifying HR.

    """

    answer = generate_response(

        email,

        context

    )

    print()

    print("=" * 60)

    print(answer)

    print("=" * 60)