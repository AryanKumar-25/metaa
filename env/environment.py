import random
import sqlite3

from env.models import Observation, Action
from env.grader import grade


class SQLRepairEnv:

    def __init__(self):
        self.tasks = [
            {
                "difficulty": "easy",
                "broken": "SELECT name FROM users WHERE age > 'twenty';",
                "correct": "SELECT name FROM users WHERE age > 20;"
            },
            {
                "difficulty": "medium",
                "broken": "SELECT * FROM users JOIN users;",
                "correct": "SELECT * FROM users u1 JOIN users u2 ON u1.id = u2.id;"
            },
            {
                "difficulty": "hard",
                "broken": "SELECT name FROM users WHERE age = (SELECT MAX(age));",
                "correct": "SELECT name FROM users WHERE age = (SELECT MAX(age) FROM users);"
            }
        ]

    def reset(self):
        self.task = random.choice(self.tasks)

        return Observation(
            broken_query=self.task["broken"],
            difficulty=self.task["difficulty"]
        )

    def step(self, action: Action):
        query = action.query

        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE users(id INT, name TEXT, age INT)")
        cursor.execute("INSERT INTO users VALUES (1, 'A', 18), (2, 'B', 25)")

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            error = None
        except Exception as e:
            result = None
            error = str(e)

        reward = grade(
            predicted=query,
            expected_query=self.task["correct"],
            result=result,
            error=error
        )

        return Observation(
            broken_query=query,
            difficulty=self.task["difficulty"],
            result=result,
            error=error
        ), reward, reward == 1.0, {}