import logging

try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False
    Groq = None

from app.config import GROQ_API_KEY

logger = logging.getLogger(__name__)


class PrimaryLLM:

    def __init__(self):
        if not HAS_GROQ:
            raise RuntimeError(
                "groq is not installed. "
                "Install it with: pip install groq"
            )

        self.client = Groq(

            api_key=GROQ_API_KEY

        )

        self.model = "llama-3.3-70b-versatile"

    # ===================================

    def generate(

        self,

        prompt

    ):

        try:

            response = self.client.chat.completions.create(

                model=self.model,

                messages=[

                    {

                        "role": "system",

                        "content":

                        "You are an expert AI Email Assistant."

                    },

                    {

                        "role": "user",

                        "content": prompt

                    }

                ],

                temperature=0.2,

                max_tokens=512

            )

            answer = response.choices[0].message.content

            logger.info("Primary LLM Success")

            return answer

        except Exception as e:

            logger.error(

                f"Primary LLM Failed : {e}"

            )

            raise e


# Lazy loading of primary LLM
_primary_llm = None

def get_primary_llm():
    global _primary_llm
    if _primary_llm is None:
        _primary_llm = PrimaryLLM()
    return _primary_llm

primary_llm = None  # Will be loaded lazily


if __name__ == "__main__":

    prompt = "Write a professional leave approval email."

    print(

        primary_llm.generate(

            prompt

        )

    )
