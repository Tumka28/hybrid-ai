import streamlit as st
import media_edit  # 🎬 Видео засварлагч модулийг дуудаж байна

st.sidebar.title("🎛 Нэмэлт хэрэгсэл")
menu = st.sidebar.radio("Сонгох:", ["🤖 AI чат", "🎬 Видео засварлагч"])

if menu == "🎬 Видео засварлагч":
    media_edit.media_edit_ui()
else:
    st.header("🤖 Түмэнжаргалын Hybrid AI System")
    st.write("Local Ollama + Memory + Chat Interface")
import streamlit as st
import requests
import json
import os
from datetime import datetime

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MEMORY_FILE = "memory/memory.json"

# --- Туслах функцүүд ---
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        os.makedirs("memory", exist_ok=True)
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

def query_ollama(prompt):
    payload = {"model": "llama3.1", "prompt": prompt}
    response = requests.post(OLLAMA_URL, json=payload, stream=True)
    reply = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                reply += data["response"]
    return reply.strip()

# --- UI хэсэг ---
st.set_page_config(page_title="Hybrid AI Assistant", layout="wide")
st.title("🤖 Түмэнжаргалын Hybrid AI System")
st.markdown("**Local Ollama + Memory + Streamlit Interface**")

memory = load_memory()

with st.sidebar:
    st.header("🧠 AI Memory")
    if st.button("Clear Memory"):
        save_memory([])
        st.success("AI санах ойг цэвэрлэлээ ✅")
    st.write("Өмнөх ярилцлагууд:")
    for item in memory[-5:]:
        st.write(f"- {item['user'][:40]}...")

user_input = st.text_area("🗨️ Текстээ оруулна уу:", placeholder="AI-д асуулт эсвэл команд бич...")
if st.button("Илгээх"):
    st.write("⏳ Хариулж байна...")
    ai_response = query_ollama(user_input)
    st.markdown(f"### 🤖 Хариулт:\n{ai_response}")

    # Санах ой хадгалах
    memory.append({"time": str(datetime.now()), "user": user_input, "ai": ai_response})
    save_memory(memory)
    st.success("Хариулт амжилттай хадгалагдлаа ✅")
import streamlit as st
from hybrid_chatbot import chat_with_ai  # эсвэл өөр гол функцээ энд импортлоорой

def main():
    st.title("🤖 Hybrid AI Assistant")
    st.write("Тавтай морил Tumka28! 🚀")
    
    user_input = st.text_input("Ямар асуулт байна?")
    if st.button("AI хариулах"):
        if user_input:
            response = chat_with_ai(user_input)
            st.success(response)
        else:
            st.warning("Юу бичихээ оруулна уу!")

if __name__ == "__main__":
    main()
