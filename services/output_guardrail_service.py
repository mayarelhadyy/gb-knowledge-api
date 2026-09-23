from services.llm_service import generate_answer


VALIDATION_SYSTEM_PROMPT = """
You are a strict answer-grounding validator.

Your task is to determine whether the provided ANSWER is fully
supported by the provided CONTEXT.

Rules:

1. Every factual claim in the ANSWER must be supported by the CONTEXT.

2. Do not use outside knowledge.

3. Paraphrasing is allowed if the meaning remains supported
   by the CONTEXT.

4. If the ANSWER contains any unsupported factual claim,
   return exactly:
   UNSUPPORTED

5. If all factual claims are supported by the CONTEXT,
   return exactly:
   SUPPORTED

6. Do not explain your decision.

Return only one word:
SUPPORTED
or
UNSUPPORTED
""".strip()


def validate_answer(
    answer: str,
    context: str
):
    user_message = f"""
--- BEGIN CONTEXT ---

{context}

--- END CONTEXT ---

--- BEGIN ANSWER ---

{answer}

--- END ANSWER ---
""".strip()

    validation_result = generate_answer(
        VALIDATION_SYSTEM_PROMPT,
        user_message
    )

    validation_result = validation_result.strip().upper()

    return validation_result == "SUPPORTED"