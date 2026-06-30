from pydantic import BaseModel, Field


class EmailRequest(BaseModel):

    email: str = Field(

        ...,

        min_length=5,

        description="Incoming Email Text",

        example="""
Hi HR,

I am not feeling well today.

Kindly grant me one day sick leave.

Thank you.

Regards,
Vinay
"""
    )

    class Config:

        json_schema_extra = {

            "example": {

                "email": """
Hi HR,

I am not feeling well today.

Kindly approve my sick leave.

Regards,
Vinay
"""
            }

        }