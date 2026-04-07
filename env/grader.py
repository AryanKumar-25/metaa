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
    if error:
        return 0.0

    exp_result, _ = execute(expected_query)

    if result == exp_result:
        return 1.0

    return 0.5