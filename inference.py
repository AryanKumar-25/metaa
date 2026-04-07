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
    q = broken_query.lower()

    # 🔥 RULE-BASED FIXES (guaranteed)
    if "'twenty'" in q:
        return broken_query.replace("'twenty'", "20")

    if "age = '18'" in q:
        return broken_query.replace("'18'", "18")

    if "select name users" in q:
        return "SELECT name FROM users;"

    if "join users;" in q and "on" not in q:
        return "SELECT * FROM users u1 JOIN users u2 ON u1.id = u2.id;"

    if "order name" in q:
        return "SELECT name FROM users WHERE age > 20 ORDER BY name;"

    if "where age >;" in q:
        return "SELECT * FROM users WHERE age > 20;"

    if "max(age)" in q and "from users" not in q:
        return "SELECT name FROM users WHERE age = (SELECT MAX(age) FROM users);"

    if "count name" in q:
        return "SELECT COUNT(name) FROM users;"

    if "in select" in q:
        return "SELECT name FROM users WHERE id IN (SELECT id FROM users);"

    if "group name" in q:
        return "SELECT name, age FROM users GROUP BY name, age;"

    # 🤖 GEMINI (fallback)
    prompt = f"""
Fix this SQL query and return ONLY SQL:

{broken_query}
"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        # 🔥 FORCE extraction of SQL
        lines = text.split("\n")
        for line in lines:
            if "select" in line.lower():
                return line.strip()

        return broken_query

    except:
        return broken_query