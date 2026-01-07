from ollama_client import ask_llm
import tools
from notifier import notify_admin 

INTENT_PROMPT= """You are an AI Website Guardian. 
Your job is to classify the user message into any one of the following categories:
-Spam -Bug -Suggestion -Abuse -Unknown. You have to reply ONLY with the category name. Message:"""

def decide_intent(message: str) -> str:
    prompt = INTENT_PROMPT + message
    intent = ask_llm(prompt).lower()

    allowed = {"spam", "bug", "suggestion", "abuse", "unknown"}
    return intent if intent in allowed else "unknown"


def act(intent: str, message: str):
    if intent == "spam":
        return tools.handle_spam(message)

    if intent == "bug":
        return tools.handle_bug(message)

    if intent == "suggestion":
        return tools.handle_suggestion(message)

    if intent == "abuse":
        notify_admin(intent, message)
        return tools.handle_spam(message)

    return tools.handle_unknown(message)


if __name__ == "__main__":
    print(" AI Website Guardian running...\n")

    while True:
        user_message = input("Website message (type 'exit'): ")
        if user_message.lower() == "exit":
            break

        intent = decide_intent(user_message)
        result = act(intent, user_message)

        print(f"Intent: {intent}")
        print(f"Action: {result.detail}\n")

