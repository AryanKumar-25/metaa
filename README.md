---
title: SQL Repair Environment
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# 🎮 AI SQL Repair Environment

An AI training environment where an agent repairs incorrect SQL queries and is scored based on correctness.

## 🚀 Features
- OpenEnv compliant (step/reset/state)
- Easy → Medium → Hard tasks
- Reward-based scoring
- SQLite execution
- Hugging Face deployment

## ▶️ Example Output

🎯 Episode 1 | Difficulty: easy  
🧩 Broken Query:  
SELECT name age FROM users  

🤖 AI Fixed Query:  
SELECT name, age FROM users  

🏆 Reward: 1.0  

## 🧠 Model Used
google/flan-t5-base