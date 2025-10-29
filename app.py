import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# ----------------------------
# Session state
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "first_question_pending" not in st.session_state:
    st.session_state.first_question_pending = True

# ----------------------------
# Gemini API call
# ----------------------------
def ask_gemini_api(prompt: str, user_name: str) -> str:
    try:
        persona_instruction = (
            f"You are a Christian faithful girl named BIBLIOBOT. "
            f"Address the user by their name: {user_name}. "
            "Only answer biblical questions in Roman Urdu + English. "
            "Always reference the Bible and be kind. "
            "Do NOT include Islamic or extra-biblical content."
        )
        st.session_state.chat_session.send_message(persona_instruction)
        response = st.session_state.chat_session.send_message(prompt)
        return getattr(response, "text", str(response))  # plain text only
    except Exception as e:
        return f"Error: {str(e)}"

# ----------------------------
# UI
# ----------------------------
st.markdown("<h1 style='text-align:center; font-size:56px;'>BIBLIOBOT</h1>", unsafe_allow_html=True)
st.markdown("""
<style>
.chat-box {min-height:300px; max-height:520px; overflow-y:auto; padding:14px; border:1px solid #ddd; border-radius:12px; background-color:#f7f7f8;}
.message-bubble {padding:10px 14px; border-radius:18px; max-width:70%; clear:both; box-shadow:0 1px 2px rgba(0,0,0,0.12); word-wrap: break-word; white-space: pre-wrap;}
.user { float:right; margin:6px 0 6px auto; background-color:#111111; color:white; }
.bot { float:left; margin:6px auto 6px 0; background-color:white; color:black; }
.timestamp { font-size:10px; color:gray; float:right; margin-left:8px; }
</style>
""", unsafe_allow_html=True)

chat_container = st.empty()
user_input = st.text_input("", placeholder="Type your Biblical question here...", key="input_box")

# ----------------------------
# Handle user input
# ----------------------------
if user_input.strip():
    now = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({"type": "right", "content": user_input, "time": now})

    if st.session_state.first_question_pending:
        # ask for name (no "Beta") + answer first question
        st.session_state.user_name = user_input
        reply = ask_gemini_api(user_input, st.session_state.user_name)
        st.session_state.messages.append({"type": "left", "content": reply, "time": now})
        st.session_state.first_question_pending = False
    else:
        reply = ask_gemini_api(user_input, st.session_state.user_name)
        st.session_state.messages.append({"type": "left", "content": reply, "time": now})

# ----------------------------
# Render messages (plain text only)
# ----------------------------
chat_html = ""
for msg in st.session_state.messages:
    cls = "message-bubble user" if msg["type"]=="right" else "message-bubble bot"
    chat_html += f'<div class="{cls}">{msg["content"]}<br><span class="timestamp">{msg["time"]}</span></div>'
chat_html += "<div style='clear:both;'></div>"
chat_container.markdown(f'<div class="chat-box">{chat_html}</div>', unsafe_allow_html=True)

# ----------------------------
# Auto-scroll
# ----------------------------
st.markdown("""
<script>
var chatBox = document.querySelector('.chat-box');
if(chatBox){ chatBox.scrollTop = chatBox.scrollHeight; }
</script>
""", unsafe_allow_html=True)
