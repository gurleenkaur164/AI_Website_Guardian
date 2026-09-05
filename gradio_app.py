import gradio as gr
from main import run_agent
from db import get_stats, get_recent

def guardian_ui(user_message):
    if not user_message or not user_message.strip():
        return "Please enter a message.", "", ""

    try:
        result = run_agent(user_message)

        summary = f"**Result:** {result['summary']}"

        visitor_reply = ""
        if result.get("visitor_reply"):
            visitor_reply = f"**Reply to visitor:**\n\n{result['visitor_reply']}"

        trace_lines = []
        for t in result["trace"]:
            if t["tool"] == "thinking":
                trace_lines.append(f"**Step {t['step']}** — Reasoning:\n> {t['result'][:200]}")
            elif t["tool"] == "check_prompt_injection":
                icon = "BLOCKED" if "BLOCKED" in str(t["result"]) else "Safe"
                trace_lines.append(f"**Step {t['step']}** — `check_prompt_injection` → {icon}")
            else:
                trace_lines.append(f"**Step {t['step']}** — `{t['tool']}` → {str(t['result'])[:150]}")

        trace_md = "\n\n".join(trace_lines) if trace_lines else "No steps recorded."

        return summary, visitor_reply, trace_md

    except Exception as e:
        return f"Error: {str(e)}", "", ""

def load_dashboard():
    stats = get_stats()
    recent = get_recent(limit=15)

    if stats["total"] == 0:
        return "No messages recorded yet.", ""

    lines = [f"### Total Messages: {stats['total']}\n"]

    lines.append("#### By Intent")
    for intent, count in stats["by_intent"].items():
        bar = "#" * min(count, 30)
        lines.append(f"- **{intent}**: {count} {bar}")

    lines.append("\n#### By Severity")
    for severity, count in stats["by_severity"].items():
        bar = "#" * min(count, 30)
        lines.append(f"- **{severity}**: {count} {bar}")

    stats_md = "\n".join(lines)

    if recent:
        table_lines = ["| Time | Intent | Severity | Message |", "|---|---|---|---|"]
        for r in recent:
            ts = r["timestamp"][:19].replace("T", " ")
            msg = r["original_message"][:60].replace("|", "\\|")
            table_lines.append(f"| {ts} | {r['intent']} | {r['severity']} | {msg} |")
        recent_md = "\n".join(table_lines)
    else:
        recent_md = "No recent messages."

    return stats_md, recent_md

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# AI Website Guardian")
    gr.Markdown("Agentic AI with tool calling, prompt injection detection, response generation, and analytics")

    with gr.Tabs():
        with gr.TabItem("Analyse"):
            input_box = gr.Textbox(
                label="Website Visitor Message",
                placeholder="Type a message like a real website user...",
                lines=3
            )
            analyze_button = gr.Button("Analyse Message", variant="primary")
            summary_box = gr.Markdown(label="Result")
            reply_box = gr.Markdown(label="Visitor Reply")
            trace_box = gr.Markdown(label="Agent Reasoning Trace")

            analyze_button.click(
                fn=guardian_ui,
                inputs=input_box,
                outputs=[summary_box, reply_box, trace_box]
            )

        with gr.TabItem("Dashboard"):
            refresh_button = gr.Button("Refresh Dashboard", variant="secondary")
            stats_box = gr.Markdown(label="Statistics")
            recent_box = gr.Markdown(label="Recent Messages")

            refresh_button.click(
                fn=load_dashboard,
                inputs=[],
                outputs=[stats_box, recent_box]
            )
            demo.load(fn=load_dashboard, outputs=[stats_box, recent_box])

demo.launch()
