TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "log_spam",
            "description": "Log a message identified as spam. Use when the message is unsolicited promotion, advertising, or irrelevant content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "The spam message to log"},
                    "severity": {"type": "string", "enum": ["low", "medium", "high"], "description": "Severity level"}
                },
                "required": ["message", "severity"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "log_bug",
            "description": "Log a bug report from a user. Use when the message describes a technical issue, error, or broken feature.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "The bug report to log"},
                    "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"], "description": "Bug severity level"}
                },
                "required": ["message", "severity"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "log_suggestion",
            "description": "Log a feature suggestion or feedback from a user. Use when the message proposes an improvement or new feature.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "The suggestion to log"},
                    "severity": {"type": "string", "enum": ["low", "medium", "high"], "description": "Priority level"}
                },
                "required": ["message", "severity"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "notify_admin",
            "description": "Send an alert to the admin. Use for abuse, threats, or critical issues that need immediate human attention.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {"type": "string", "description": "Why the admin is being notified"},
                    "message": {"type": "string", "description": "The original message"}
                },
                "required": ["reason", "message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_duplicates",
            "description": "Search for similar past messages to check for duplicate reports. Use before logging a bug to see if it was already reported.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "Keyword to search for in past messages"}
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "done",
            "description": "Call this when you have finished processing the message and all necessary actions are complete.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string", "description": "Brief summary of what was done"}
                },
                "required": ["summary"]
            }
        }
    }
]
