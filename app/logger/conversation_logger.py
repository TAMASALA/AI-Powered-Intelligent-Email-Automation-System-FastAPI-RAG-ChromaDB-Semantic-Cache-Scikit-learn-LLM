import json
import uuid
from pathlib import Path
from datetime import datetime

from app.config import HISTORY_DIR


CONVERSATION_DIR = HISTORY_DIR / "conversations"

CONVERSATION_DIR.mkdir(

    parents=True,

    exist_ok=True

)


# =====================================================
# Save Conversation
# =====================================================

def save_conversation(

    email,

    classification,

    context,

    response,

    source

):

    data = {

        "id": str(uuid.uuid4()),

        "timestamp": datetime.now().strftime(

            "%Y-%m-%d %H:%M:%S"

        ),

        "email": email,

        "classification": classification,

        "rag_context": context,

        "response": response,

        "generated_by": source

    }

    filename = (

        datetime.now().strftime(

            "%Y%m%d_%H%M%S"

        )

        + "_"

        + str(uuid.uuid4())[:8]

        + ".json"

    )

    filepath = CONVERSATION_DIR / filename

    with open(

        filepath,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            data,

            f,

            indent=4,

            ensure_ascii=False

        )

    return filepath


# =====================================================
# Test
# =====================================================

if __name__ == "__main__":

    save_conversation(

        email="Need one day sick leave.",

        classification="HAM",

        context="Leave policy",

        response="Leave Approved.",

        source="Primary LLM"

    )

    print("Conversation Saved")