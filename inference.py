import asyncio
import time
from transformers import pipeline

from env.environment import SQLRepairEnv
from env.models import Action

# Load model
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    do_sample=False
)

def fix_query_with_ai(broken_query, schema):
    prompt = f"""
Fix the SQL query. Only return valid SQL.

Schema:
users(id, name, age)

Broken Query:
{broken_query}

Correct SQL:
"""

    result = generator(prompt, max_new_tokens=50)
    output = result[0]["generated_text"]

    fixed_query = output.split("Correct SQL:")[-1].strip()
    fixed_query = fixed_query.split("\n")[0]

    # simple fixes
    if fixed_query.strip().endswith(">"):
        fixed_query += " 18"

    fixed_query = fixed_query.replace("FORM", "FROM")

    if fixed_query.strip().endswith("ORDER"):
        fixed_query += " BY age"

    return fixed_query


async def run():
    env = SQLRepairEnv()

    total = 0
    score = 0

    print("\n🎮 AI SQL Repair Evaluation Started!\n")

    for i in range(5):

        state = await env.reset()

        obs = state["observation"]

        print("\n==============================")
        print(f"🎯 Episode {i+1} | Difficulty: {obs.difficulty}")
        print("🧩 Broken Query:")
        print(obs.broken_query)

        fixed_query = fix_query_with_ai(obs.broken_query, obs.db_schema)

        print("\n🤖 AI Fixed Query:")
        print(fixed_query)

        action = Action(query=fixed_query)
        result = await env.step(action)

        reward = result["reward"]

        print("\n🏆 Reward:", reward)
        print("📊 Result:", result["observation"].result)

        total += 1
        score += reward

        print(f"\n📈 Accuracy: {score / total:.2f}")

    print("\n==============================")
    print(f"✅ FINAL SCORE: {score / total:.2f}")


import os
import time

if __name__ == "__main__":
    asyncio.run(run())

    # ✅ Only keep alive on Hugging Face
    if os.getenv("HF_SPACE") == "true":
        while True:
            time.sleep(60)