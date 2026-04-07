import sqlite3


def execute(query):
    try:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE users(id INT, name TEXT, age INT)")
        cursor.execute("INSERT INTO users VALUES (1, 'A', 18), (2, 'B', 25)")

        cursor.execute(query)
        return cursor.fetchall(), None

    except Exception as e:
        return None, str(e)


def grade(predicted, expected_query, result, error):
    # ❌ syntax error
    if error:
        return 0.0

    exp_result, _ = execute(expected_query)

    # ✅ exact match
    if result == exp_result:
        if predicted.strip().lower() == expected_query.strip().lower():
            return 1.0
        else:
            return 0.8  # correct result but different query

    # ⚠️ partial
    return 0.5