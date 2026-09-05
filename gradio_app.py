import gradio as gr
from main import run_agent

def guardian_ui(user_message):
    if not user_message or not user_message.strip():
        return "Please enter a message.", ""

    try:
        result = run_agent(user_message)

        summary = f"**Result:** {result['summary']}"

        trace_lines = []
        for t in result["trace"]:
            if t["tool"] == "thinking":
                trace_lines.append(f"**Step {t['step']}** — Reasoning:\n> {t['result'][:200]}")
            else:
                trace_lines.append(f"**Step {t['step']}** — `{t['tool']}` → {t['result']}")

        trace_md = "\n\n".join(trace_lines) if trace_lines else "No steps recorded."

        return summary, trace_md

    except Exception as e:
        return f"Error: {str(e)}", ""

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# AI Website Guardian")
    gr.Markdown("Agentic AI system with tool calling, multi-step reasoning, and SQLite storage")

    input_box = gr.Textbox(
        label="Website Visitor Message",
        placeholder="Type a message like a real website user...",
        lines=3
    )

    analyze_button = gr.Button("Analyse Message")

    summary_box = gr.Markdown(label="Result")
    trace_box = gr.Markdown(label="Agent Reasoning Trace")

    analyze_button.click(
        fn=guardian_ui,
        inputs=input_box,
        outputs=[summary_box, trace_box]
    )

demo.launch()
