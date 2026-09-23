from services.chat_service import (
    create_conversation,
    add_message,
    get_history,
    rewrite_question
)


conversation_id = create_conversation()

add_message(
    conversation_id,
    "user",
    "What types of leave are available?"
)

add_message(
    conversation_id,
    "assistant",
    "Annual leave, sick leave, emergency leave, and parental leave."
)

history = get_history(
    conversation_id
)

rewritten = rewrite_question(
    "How do I request it?",
    history
)

print("Conversation ID:")
print(conversation_id)

print("\nHistory:")
print(history)

print("\nOriginal:")
print("How do I request it?")

print("\nRewritten:")
print(rewritten)