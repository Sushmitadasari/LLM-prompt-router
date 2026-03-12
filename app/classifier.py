import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


CLASSIFIER_PROMPT = """
Your task is to classify the user's intent.

Choose ONE label from the following list:
code, data, writing, career, unclear

Respond ONLY with a JSON object using this schema:

{
"intent": "label",
"confidence": float_between_0_and_1
}

Do not include explanations or text outside JSON.
"""


def classify_intent(message: str) -> dict:

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": CLASSIFIER_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        result = json.loads(content)

        intent = result.get("intent", "unclear")
        confidence = float(result.get("confidence", 0.0))

        return {
            "intent": intent,
            "confidence": confidence
        }

    except Exception:
        return {
            "intent": "unclear",
            "confidence": 0.0
        }