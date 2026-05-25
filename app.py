import streamlit as st
from groq import Groq
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Health Chatbot", page_icon="🩺")

st.title("🩺 Health Assistant Chatbot")
st.write("Ask general health questions. Not a replacement for a doctor.")

# =========================
# GROQ API KEY (HUGGING FACE SAFE)
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("Missing GROQ_API_KEY. Add it in Hugging Face Secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# =========================
# MODEL
# =========================
MODEL_NAME = "llama-3.1-8b-instant"

# =========================
# SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a helpful and safe medical assistant. "
        "Provide only general health information. "
        "Do NOT diagnose or prescribe medicines. "
        "Always recommend consulting a doctor for serious conditions. "
        "Keep responses short, clear, and simple."
    )
}

# =========================
# SESSION STATE INIT (SAFE FOR HF)
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = [SYSTEM_PROMPT]

# =========================
# CHAT HISTORY DISPLAY
# =========================
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# =========================
# CHAT INPUT
# =========================
user_input = st.chat_input("Ask your health question...")

# =========================
# GROQ RESPONSE FUNCTION
# =========================
def get_response(messages):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.6,
        max_tokens=512
    )
    return response.choices[0].message.content

# =========================
# CHAT LOGIC
# =========================
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = get_response(st.session_state.messages)
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
