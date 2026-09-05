import json
from ollama_client import chat
from tool_schemas import TOOLS
from tools import execute_tool

SYSTEM_PROMPT = """You are an AI Website Guardian agent. You protect a website by analyzing visitor messages.

Your workflow:
1. Read the visitor's message carefully.
2. Determine the intent: spam, bug report, suggestion, or abuse/threat.
3. For bug reports, first use search_duplicates to check if a similar bug was already reported.
4. Use the appropriate logging tool (log_spam, log_bug, log_suggestion).
5. For abuse or threats, use notify_admin to alert the site owner.
6. When all actions are complete, call the done tool with a summary.

Always assess severity:
- low: minor or routine
- medium: affects user experience
- high: significant impact
- critical: (bugs only) system-breaking or data loss

Think step by step. You may call multiple tools in sequence."""

MAX_STEPS = 6

def run_agent(user_message):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"New website visitor message:\n\n{user_message}"},
    ]
    trace = []

    for step in range(MAX_STEPS):
        response = chat(messages, tools=TOOLS)

        if response.get("tool_calls"):
            for tool_call in response["tool_calls"]:
                name = tool_call["function"]["name"]
                args = tool_call["function"]["arguments"]

                result = execute_tool(name, args)
                trace.append({"step": step + 1, "tool": name, "args": args, "result": result})

                messages.append({"role": "assistant", "content": "", "tool_calls": [tool_call]})
                messages.append({"role": "tool", "content": str(result)})

                if name == "done":
                    return {"summary": result, "trace": trace}
        else:
            content = response.get("content", "")
            if content:
                trace.append({"step": step + 1, "tool": "thinking", "args": {}, "result": content})
                messages.append({"role": "assistant", "content": content})

    return {"summary": "Agent reached max steps without completing.", "trace": trace}


if __name__ == "__main__":
    print("AI Website Guardian running...\n")

    while True:
        user_message = input("Website message (type 'exit'): ")
        if user_message.lower() == "exit":
            break

        result = run_agent(user_message)
        print(f"\nSummary: {result['summary']}")
        print(f"Steps taken: {len(result['trace'])}")
        for t in result["trace"]:
            print(f"  Step {t['step']}: {t['tool']}({t['args']}) -> {t['result'][:100]}")
        print()
