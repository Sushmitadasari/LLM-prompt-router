import os
from openai import OpenAI

from .prompts import EXPERT_PROMPTS

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def route_and_respond(message: str, intent_data: dict) -> str:
    """
    Routes the request to the correct expert persona.
    """

    intent = intent_data.get("intent", "unclear")

    if intent == "unclear":
        return (
            "Could you clarify your request? "
            "Are you asking for help with coding, data analysis, "
            "writing improvement, or career advice?"
        )

    system_prompt = EXPERT_PROMPTS.get(intent)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()