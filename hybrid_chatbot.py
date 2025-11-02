import streamlit as st
import requests
import sqlite3
import os
from datetime import datetime

# --- Тохиргоо ---
OLLAMA_URL = "http://localhost:11434/api/generate"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # export OPENAI_API_KEY="түлхүүр"
DB_PATH = "memory.db"

# --- Санах ой үүсгэх ---
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    content TEXT,
    time TEXT
)
""")
conn.commit()

# --- Хариулт бичих функц ---
def save_memory(role, content):
    cur.execute("INSERT INTO memory (role, content, time) VALUES (?, ?, ?)",
                (role, content, str(datetime.now())))
    conn.commit()

# --- Chat лог авах ---
def load_memory():
    cur.execute("SELECT role, content FROM memory ORDER BY id DESC LIMIT 20")
    return cur.fetchall()[::-1]

# --- Ollama AI (offline) ---
def ask_ollama(prompt):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }, timeout=20)
        return response.json().get("response", "Ollama хариу ирсэнгүй.")
    except Exception as e:
        return f"Ollama алдаа: {e}"

# --- OpenAI GPT (online) ---
def ask_openai(prompt):
    try:
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}]
        }
        res = requests.post("https://api.openai.com/v1/chat/completions",
                            headers=headers, json=data, timeout=20)
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"OpenAI алдаа: {e}"

# --- Streamlit UI ---
st.set_page_config(page_title="Hybrid AI Chat", page_icon="🤖")
st.title("🤖 Hybrid AI Chat — OpenAI + Ollama")
st.write("Интернеттэй үед GPT-4 ашиглана, оффлайн үед Ollama ажиллана.")

# --- Хуучин яриаг харуулах ---
for role, msg in load_memory():
    if role == "user":
        st.markdown(f"🧑 **Та:** {msg}")
    else:
        st.markdown(f"🤖 **AI:** {msg}")

prompt = st.chat_input("Асуух зүйлээ бичнэ үү...")

if prompt:
    save_memory("user", prompt)
    with st.spinner("AI хариу боловсруулж байна..."):
        if OPENAI_API_KEY:
            reply = ask_openai(prompt)
        else:
            reply = ask_ollama(prompt)
    st.markdown(f"🤖 **AI:** {reply}")
    save_memory("assistant", reply)
import requests
import json

def chat_with_ai(prompt):
    """
    Local Ollama API эсвэл chatbot сервер рүү текст илгээж хариу авна.
    """
    try:
        url = "http://127.0.0.1:11434/api/generate"
        payload = {"model": "llama3.1", "prompt": prompt}
        response = requests.post(url, json=payload, stream=True)

        reply = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    reply += data["response"]
        return reply.strip() or "⚠️ AI-аас хариу ирсэнгүй."
    except Exception as e:
        return f"❌ Алдаа гарлаа: {e}"
