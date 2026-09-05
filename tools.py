from db import save_message, search_similar

def log_spam(message, severity="low"):
    save_message("spam", message, severity=severity, action_taken="Logged as spam")
    return f"Spam message logged with severity={severity}."

def log_bug(message, severity="low"):
    save_message("bug", message, severity=severity, action_taken="Logged as bug report")
    return f"Bug report logged with severity={severity}."

def log_suggestion(message, severity="low"):
    save_message("suggestion", message, severity=severity, action_taken="Logged as suggestion")
    return f"Suggestion logged with severity={severity}."

def notify_admin(reason, message):
    save_message("abuse", message, severity="critical", action_taken=f"Admin notified: {reason}")
    return f"Admin alerted. Reason: {reason}"

def search_duplicates(keyword):
    results = search_similar(keyword)
    if not results:
        return "No similar past messages found."
    lines = [f"- [{r['intent']}] {r['original_message'][:80]}..." for r in results]
    return f"Found {len(results)} similar message(s):\n" + "\n".join(lines)

def done(summary):
    return summary

TOOL_REGISTRY = {
    "log_spam": log_spam,
    "log_bug": log_bug,
    "log_suggestion": log_suggestion,
    "notify_admin": notify_admin,
    "search_duplicates": search_duplicates,
    "done": done,
}

def execute_tool(name, arguments):
    func = TOOL_REGISTRY.get(name)
    if not func:
        return f"Unknown tool: {name}"
    return func(**arguments)
