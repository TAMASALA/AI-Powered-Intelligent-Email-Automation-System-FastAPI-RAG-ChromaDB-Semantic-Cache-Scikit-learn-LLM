from typing import Optional

from pydantic import BaseModel


class EmailResponse(BaseModel):

    classification: str

    response: str

    source: str

    similarity_score: Optional[float] = None

    retrieved_chunks: Optional[int] = None

    status: str = "Success"

    class Config:

        json_schema_extra = {

            "example": {

                "classification": "HAM",

                "response":
                "Dear Vinay,\n\nYour sick leave request has been received and approved.\n\nRegards,\nHR Team",

                "source": "Primary LLM",

                "similarity_score": 0.94,

                "retrieved_chunks": 5,

                "status": "Success"

            }

        }


class SpamResponse(BaseModel):

    classification: str = "SPAM"

    response: str = "Spam email deleted."

    source: str = "Machine Learning"

    status: str = "Success"


class ErrorResponse(BaseModel):

    status: str = "Failed"

    error: str