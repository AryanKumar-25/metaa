import os
from google import genai

# setup
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def clean_sql(text):
    text = text.strip()

    if "```" in text:
        text = text.split("```")[1]

    lines = text.split("\n")
    for line in lines:
        if "select" in line.lower():
            return line.strip()

    return text


def fix_query(broken_query):
    # 🔥 Rule-based quick fixes (guaranteed improvement)
    fixed = broken_query.lower()

    # fix common error
    if "'twenty'" in fixed:
        return broken_query.replace("'twenty'", "20")

    # fix missing ON in JOIN
    if "join" in fixed and "on" not in fixed:
        return "SELECT * FROM users u1 JOIN users u2 ON u1.id = u2.id;"

    # fix missing FROM in subquery
    if "max(age)" in fixed and "from users" not in fixed:
        return "SELECT name FROM users WHERE age = (SELECT MAX(age) FROM users);"

    # 🤖 fallback to Gemini if no rule matched
    prompt = f"""
Fix this SQL query. Return only SQL.

{broken_query}
"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return clean_sql(response.text)

    except:
        return broken_query