import gradio as gr
from main import decide_intent, act

def guardian_ui(user_message):
    if not user_message or not user_message.strip():
        return " Please enter a message."

    try:
        intent = decide_intent(user_message)
        result = act(intent, user_message)

        
        if isinstance(result, dict):
            action = result.get("detail", str(result))
        else:
            action = str(result)

        return f"""
 Analysis Result

**Detected Intent:** `{intent.upper()}`  

**Action Taken:**  
{action}
"""

    except Exception as e:
        return f" Error occurred:\n```\n{str(e)}\n```"

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(" AI Website Guardian")
    gr.Markdown("Agentic AI Agent powered by Ollama")

    input_box = gr.Textbox(
        label="Website Visitor Message",
        placeholder="Type a message like a real website user...",
        lines=3
    )

    output_box = gr.Markdown()

    analyze_button = gr.Button("Analyse Message")
    analyze_button.click(
        fn=guardian_ui,
        inputs=input_box,
        outputs=output_box
    )

demo.launch()
