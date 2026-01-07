from tool_schemas import ToolResult
from datetime import datetime

DATA_DIR= "data"

def save_to_file(filename: str, message:str)-> ToolResult:
    path = f"{DATA_DIR}/{filename}"
    timestamp = datetime.now().isoformat()

    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

    return ToolResult(
        status="success",
        detail=f"Saved to {filename}"
    )
def handle_spam(message:str)->ToolResult:
    return save_to_file("spam.txt", message)

def handle_bug(message:str)->ToolResult:
    return save_to_file("bugs.txt", message)

def handle_suggestion(message:str)->ToolResult:
    return save_to_file("suggestions.txt", message)

def handle_unknown(message:str)->ToolResult:
    return save_to_file("unknown.txt", message)  