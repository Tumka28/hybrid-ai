import json
import os
from datetime import datetime

MEMORY_FILE = "memory/self_learning_data.json"

# --- Суралцах өгөгдлийг унших ---
def load_learning_data():
    if not os.path.exists(MEMORY_FILE):
        os.makedirs("memory", exist_ok=True)
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

# --- Шинэ туршлага хадгалах ---
def save_learning(experience):
    data = load_learning_data()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data.append({"time": timestamp, "experience": experience})
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"🧠 New learning saved at {timestamp}")

# --- AI сургалтын алгоритм (жишээ) ---
def analyze_and_learn():
    data = load_learning_data()
    if not data:
        print("⚠️ No data to learn from yet.")
        return

    print("🔍 Analyzing past experiences...")
    patterns = set()
    for d in data:
        text = d["experience"].lower()
        if "error" in text:
            patterns.add("fix_errors")
        if "optimize" in text:
            patterns.add("optimization")

    if patterns:
        print(f"✅ Learning patterns found: {', '.join(patterns)}")
    else:
        print("ℹ️ No new patterns found — AI is stable.")

# --- Тест ---
if __name__ == "__main__":
    print("🤖 Түмэнжаргалын Self-Learning систем ажиллаж байна...")
    save_learning("AI successfully connected to Ollama and memory modules.")
    analyze_and_learn()
