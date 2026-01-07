from dataclasses import dataclass

@dataclass
class ToolResult:
    status: str
    detail: str
    