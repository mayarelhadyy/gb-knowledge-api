import os
import requests


LLM_API_URL = os.getenv("LLM_API_URL")


def generate_answer(
    system_prompt: str,
    user_message: str
):
    if not LLM_API_URL:
        raise RuntimeError(
            "LLM_API_URL environment variable is not configured."
        )

    response = requests.post(
        LLM_API_URL,
        json={
            "system_prompt": system_prompt,
            "user_message": user_message
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["answer"]