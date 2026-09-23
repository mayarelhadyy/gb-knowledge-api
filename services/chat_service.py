import uuid

from services.database_service import get_connection
from services.llm_service import generate_answer


REWRITE_SYSTEM_PROMPT = """
You rewrite follow-up questions into standalone questions.

Use the conversation history only to understand references
in the current message.

Do not answer the question.

Do not add facts that are not present in the conversation.

If the current message is already a standalone question,
return it unchanged.

Return only the rewritten question.
""".strip()


def create_conversation(user_id: int):
    conversation_id = str(uuid.uuid4())

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO conversations (
            conversation_id,
            user_id
        )
        VALUES (?, ?)
        """,
        (
            conversation_id,
            user_id
        )
    )

    connection.commit()
    connection.close()

    return conversation_id


def conversation_belongs_to_user(
    conversation_id: str,
    user_id: int
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT conversation_id
        FROM conversations
        WHERE conversation_id = ?
        AND user_id = ?
        """,
        (
            conversation_id,
            user_id
        )
    )

    conversation = cursor.fetchone()

    connection.close()

    return conversation is not None


def get_history(conversation_id: str):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        WHERE conversation_id = ?
        ORDER BY id ASC
        """,
        (conversation_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    history = []

    for role, content in rows:
        history.append({
            "role": role,
            "content": content
        })

    return history


def add_message(
    conversation_id: str,
    role: str,
    content: str
):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO messages (
            conversation_id,
            role,
            content
        )
        VALUES (?, ?, ?)
        """,
        (
            conversation_id,
            role,
            content
        )
    )

    connection.commit()
    connection.close()


def rewrite_question(
    message: str,
    history: list
):
    if not history:
        return message

    history_text = ""

    for item in history:
        history_text += (
            f"{item['role']}: "
            f"{item['content']}\n"
        )

    user_message = f"""
CONVERSATION HISTORY:

{history_text}

CURRENT MESSAGE:

{message}
""".strip()

    rewritten_question = generate_answer(
        REWRITE_SYSTEM_PROMPT,
        user_message
    )

    return rewritten_question.strip()