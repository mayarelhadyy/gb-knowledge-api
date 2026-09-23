from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from dependencies import get_current_user
from models import ChatRequest
from services.chat_service import (
    create_conversation,
    get_history,
    add_message,
    rewrite_question,
    conversation_belongs_to_user
)
from services.rag_service import generate_rag_answer


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):

    conversation_id = request.conversation_id
    user_id = current_user["id"]

    # New conversation
    if not conversation_id:
        conversation_id = create_conversation(
            user_id
        )

    # Existing conversation
    else:
        allowed = conversation_belongs_to_user(
            conversation_id,
            user_id
        )

        if not allowed:
            raise HTTPException(
                status_code=403,
                detail="You do not have access to this conversation"
            )

    history = get_history(
        conversation_id
    )

    standalone_question = rewrite_question(
        request.message,
        history
    )

    answer = generate_rag_answer(
        standalone_question
    )

    add_message(
        conversation_id,
        "user",
        request.message
    )

    add_message(
        conversation_id,
        "assistant",
        answer
    )

    return {
        "conversation_id": conversation_id,
        "answer": answer
    }