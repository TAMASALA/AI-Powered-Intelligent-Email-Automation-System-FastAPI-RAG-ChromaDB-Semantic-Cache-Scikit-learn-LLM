from datetime import datetime


def build_prompt(

    email: str,

    context: str

) -> str:

    prompt = f"""
You are an intelligent AI Email Assistant.

Today's Date:
{datetime.now().strftime("%d-%m-%Y")}

===============================
Company Knowledge
===============================

{context}

===============================
Incoming Email
===============================

{email}

===============================
Instructions
===============================

1. Read the company knowledge carefully.

2. Reply professionally.

3. Use company policy whenever applicable.

4. Keep the response concise.

5. Never generate fake information.

6. If the context is empty,
reply politely using general
business communication.

7. Output ONLY the email reply.

===============================
Professional Email Reply
===============================
"""

    return prompt


if __name__ == "__main__":

    email = "I need sick leave tomorrow."

    context = "Employees may apply for sick leave through HR."

    print(build_prompt(email, context))