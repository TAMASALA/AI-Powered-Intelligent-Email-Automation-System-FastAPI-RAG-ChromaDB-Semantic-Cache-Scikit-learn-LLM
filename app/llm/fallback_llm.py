import logging

try:
    import ollama
    HAS_OLLAMA = True
except ImportError:
    HAS_OLLAMA = False
    ollama = None

logger = logging.getLogger(__name__)


class FallbackLLM:

    def __init__(self):
        if not HAS_OLLAMA:
            raise RuntimeError(
                "ollama is not installed. "
                "Install it with: pip install ollama"
            )

        # Change if you use another Ollama model
        self.model = "llama3.2"

        # Examples:
        # "llama3"
        # "llama3.1"
        # "deepseek-r1:7b"
        # "mistral"

    # =======================================

    def generate(self, prompt):

        try:

            response = ollama.chat(

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

                ]

            )

            answer = response["message"]["content"]

            logger.info("Fallback LLM Success")

            return answer

        except Exception as e:

            logger.error(f"Fallback LLM Failed : {e}")

            raise RuntimeError(
                "Fallback LLM Failed."
            )


# Lazy loading of fallback LLM
_fallback_llm = None

def get_fallback_llm():
    global _fallback_llm
    if _fallback_llm is None:
        _fallback_llm = FallbackLLM()
    return _fallback_llm

fallback_llm = None  # Will be loaded lazily


if __name__ == "__main__":

    prompt = "Write a professional sick leave reply."

    print(

        get_fallback_llm().generate(prompt)

    )