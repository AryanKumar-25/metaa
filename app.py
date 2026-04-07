import gradio as gr

from env.environment import SQLRepairEnv
from env.models import Action
from inference import fix_query


def run_demo():
    env = SQLRepairEnv()

    obs = env.reset()

    broken = obs.broken_query
    difficulty = obs.difficulty

    fixed = fix_query(broken)

    observation, reward, done, _ = env.step(
        Action(query=fixed)
    )

    output = observation.result if observation.result else observation.error

    return (
        f"{broken}  (Difficulty: {difficulty})",
        fixed,
        str(output),
        reward
    )


with gr.Blocks() as demo:
    gr.Markdown("# 🧠 SQL Repair AI Agent")

    btn = gr.Button("🚀 Run AI Fix")

    broken = gr.Textbox(label="Broken SQL")
    fixed = gr.Textbox(label="Fixed SQL")
    result = gr.Textbox(label="Result / Error")
    reward = gr.Number(label="Reward")

    btn.click(
        fn=run_demo,
        inputs=[],
        outputs=[broken, fixed, result, reward]
    )


demo.launch()