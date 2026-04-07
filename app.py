import gradio as gr

from env.environment import SQLRepairEnv
from env.models import Action
from inference import fix_query

env = SQLRepairEnv()
current_obs = None
score_total = 0
attempts = 0


# -----------------------
# 🎯 Difficulty Color
# -----------------------
def format_difficulty(diff):
    if diff == "easy":
        return f"🟢 EASY"
    elif diff == "medium":
        return f"🟡 MEDIUM"
    else:
        return f"🔴 HARD"


# -----------------------
# 🔄 Next Question
# -----------------------
def next_question():
    global current_obs

    current_obs = env.reset()

    return (
        f"{current_obs.broken_query}",
        format_difficulty(current_obs.difficulty),
        "",
        "",
        0.0,
        f"{score_total}/{attempts}" if attempts else "0/0"
    )


# -----------------------
# 🚀 Run AI Fix
# -----------------------
def run_demo():
    global current_obs, score_total, attempts

    if current_obs is None:
        current_obs = env.reset()

    broken = current_obs.broken_query
    difficulty = current_obs.difficulty

    fixed = fix_query(broken)

    observation, reward, done, _ = env.step(
        Action(query=fixed)
    )

    output = observation.result if observation.result else observation.error

    # update score
    attempts += 1
    score_total += reward

    return (
        broken,
        format_difficulty(difficulty),
        fixed,
        str(output),
        reward,
        f"{round(score_total,2)}/{attempts}"
    )


# -----------------------
# 🎨 UI DESIGN
# -----------------------
with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    # 🧠 SQL Repair AI Agent  
    ### Fix broken SQL queries using Open AI 
    """)

    with gr.Row():
        btn_next = gr.Button("🔄 Next Question", variant="secondary")
        btn_run = gr.Button("🚀 Run AI Fix", variant="primary")

    with gr.Row():
        difficulty = gr.Textbox(label="📊 Difficulty", interactive=False)
        score = gr.Textbox(label="🏆 Score (Total/Attempts)", interactive=False)

    broken = gr.Textbox(label="❌ Broken SQL", lines=3)
    fixed = gr.Textbox(label="🤖 Fixed SQL", lines=3)
    result = gr.Textbox(label="📊 Output / Error", lines=3)
    reward = gr.Number(label="⭐ Reward (0–1)")

    # Actions
    btn_next.click(
        fn=next_question,
        inputs=[],
        outputs=[broken, difficulty, fixed, result, reward, score]
    )

    btn_run.click(
        fn=run_demo,
        inputs=[],
        outputs=[broken, difficulty, fixed, result, reward, score]
    )

demo.launch()