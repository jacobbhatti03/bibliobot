import streamlit as st
import time
from datetime import datetime
from src.ui import header
from src.auth import sidebar_login_ui, require_google_login
from src.storage import init_chat, add, get, clear
from src.llm import reply
from src.safety import is_scripture_related, gentle_redirect
from src.notes import add_note, format_notes_for_prompt

# ---------------- SESSION STATE INIT ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "awaiting_reply" not in st.session_state:
    st.session_state.awaiting_reply = False
    
st.set_page_config(
    page_title="BiblioBot",
    page_icon="assets/icon.png",
    layout="wide"
)

st.write("datetime exists:", "datetime" in globals())
def send_message(text):
    now = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({
        "role": "user",
        "content": text,
        "time": now
    })

# Header + auth UI
header()
sidebar_login_ui()

# Enforce login first
user = require_google_login()
user_id = user.email  # stable enough for now

# Sidebar controls + notes (keep inside sidebar)
with st.sidebar:
    st.divider()
    if st.button("Clear chat"):
        clear(user_id)
        st.rerun()

    st.divider()
    st.subheader("Scripture Notes (learn)")
    note_title = st.text_input("Title", placeholder="e.g., Romans 8 – Hope")
    note_text = st.text_area("Write your scripture-based note", height=100)

    if st.button("Save note"):
        if note_text.strip():
            add_note(user_id, note_title, note_text)
            st.success("Saved ✅")
        else:
            st.warning("Write something first.")


# -------- Chat UI --------
st.subheader("Chat")

init_chat(user_id)

# Show history
for m in get(user_id):
    with st.chat_message(m["role"]):
        st.write(m["content"])

# Input (prompt is defined here)
prompt = st.chat_input("Ask a Bible / apologetics question...")

# Process only when user sends
if prompt:
    add("user", prompt, user_id)
    with st.chat_message("user"):
        st.write(prompt)

    if not is_scripture_related(prompt):
        response = gentle_redirect(prompt)
    else:
        notes_context = format_notes_for_prompt(user_id)

        full_prompt = f"""
You are BiblioBot: a Bible + apologetics assistant.
Tone: gentle, respectful, non-judgmental.
Stay scripture-grounded. If the user is mistaken, correct kindly using scripture.
User notes may contain mistakes; verify with scripture and correct gently.

{notes_context}

User question: {prompt}
"""
        response = reply(full_prompt)

    add("assistant", response, user_id)
    with st.chat_message("assistant"):
        st.write(response)

# ----------------------------
# Page Config (Custom Name + Icon)
# ----------------------------

# ----------------------------
# Session State
# ----------------------------


if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "awaiting_reply" not in st.session_state:
    st.session_state.awaiting_reply = False

if "current_input" not in st.session_state:
    st.session_state.current_input = ""
    
if not is_scripture_related(prompt):
    response = gentle_redirect(prompt)
else:
    notes_context = format_notes_for_prompt(user_id)

    full_prompt = f"""
You are BiblioBot: a Bible + apologetics assistant.
Tone: gentle, respectful, non-judgmental.
Stay scripture-grounded. If the user asks off-topic, invite them to reframe biblically.
User notes may contain mistakes; verify with scripture and correct gently.

{notes_context}

User question: {prompt}
"""
    response = reply(full_prompt)


# ----------------------------
# Gemini API Call
# ----------------------------
def ask_gemini_api(prompt: str, user_name: str) -> str:
    try:
        persona_instruction = (
            f"You are a Christian faithful person named BIBLIOBOT. "
            f"Address the user by their name: {user_name or 'Friend'}. "
            "Only answer biblical questions in Roman Urdu + English. "
            "Always reference the Bible and be kind. "
            "Do NOT include Islamic or extra-biblical content."
            "If someone asks which religion is better , Islam or Christianity . say I dont have any personal opinion"
        )

        st.session_state.chat_session.send_message(persona_instruction)
        response = st.session_state.chat_session.send_message(prompt)
        return getattr(response, "text", str(response))
    except Exception as e:
        return f"Error: {str(e)}"


# ----------------------------
# CSS Styling
# ----------------------------
st.markdown("""
<style>
.chat-box {
    min-height: 350px;
    max-height: 520px;
    overflow-y: auto;
    padding: 14px;
    border: 1px solid #ddd;
    border-radius: 12px;
    background-color: #f7f7f8;
}
.message-bubble {
    padding: 10px 14px;
    border-radius: 18px;
    max-width: 70%;
    clear: both;
    box-shadow: 0 1px 2px rgba(0,0,0,0.12);
    word-wrap: break-word;
    white-space: pre-wrap;
}
.user { float: right; margin: 6px 0 6px auto; background-color: #111; color: white; }
.bot { float: left; margin: 6px auto 6px 0; background-color: white; color: black; }
.timestamp { font-size: 10px; color: gray; float: right; margin-left: 8px; }

/* Typing animation */
.typing {
    float: left;
    margin: 6px auto 6px 0;
    background-color: white;
    color: gray;
    border-radius: 18px;
    padding: 10px 14px;
    font-style: italic;
}
.typing span {
    display: inline-block;
    animation: blink 1.5s infinite;
}
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }

@keyframes blink {
    0% { opacity: 0.2; }
    20% { opacity: 1; }
    100% { opacity: 0.2; }
}
</style>
""", unsafe_allow_html=True)


# ----------------------------
# Chat Renderer
# ----------------------------
def render_chat(typing=False):
    chat_html = ""
    for msg in st.session_state.messages:
        cls = "message-bubble user" if msg["type"] == "right" else "message-bubble bot"
        chat_html += f'<div class="{cls}">{msg["content"]}<br><span class="timestamp">{msg["time"]}</span></div>'
    if typing:
        chat_html += '<div class="typing">BiblioBot is typing<span>.</span><span>.</span><span>.</span></div>'
    chat_html += "<div style='clear:both;'></div>"
    chat_container.markdown(f'<div class="chat-box">{chat_html}</div>', unsafe_allow_html=True)


# ----------------------------
# Send Message Logic
# ----------------------------
def send_message():
    user_input = st.session_state.current_input.strip()
    if not user_input or st.session_state.awaiting_reply:
        return

    now = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({"type": "right", "content": user_input, "time": now})
    st.session_state.awaiting_reply = True
    render_chat(typing=True)

    # Fetch reply
    with st.spinner("Thinking..."):
        reply = ask_gemini_api(user_input, st.session_state.user_name)
        time.sleep(0.4)  # small natural delay

    st.session_state.messages.append({"type": "left", "content": reply, "time": datetime.now().strftime("%I:%M %p")})
    st.session_state.awaiting_reply = False
    st.session_state.current_input = ""  # clear text box safely


# ----------------------------
# UI Header
# ----------------------------
st.markdown("<h1 style='text-align:center; font-size:56px;'>BIBLIOBOT</h1>", unsafe_allow_html=True)
chat_container = st.empty()

# ----------------------------
# Input Field + Button
# ----------------------------
col1, col2 = st.columns([7, 1])
with col1:
    st.text_input(
        "",
        placeholder="Type your Biblical question here...",
        key="current_input",
        on_change=send_message,
        label_visibility="collapsed"
    )
with col2:
    st.button("Send", use_container_width=True, on_click=send_message)

# ----------------------------
# Render Chat
# ----------------------------
render_chat(typing=st.session_state.awaiting_reply)

# ----------------------------
# Auto-scroll
# ----------------------------
st.markdown("""
<script>
var chatBox = document.querySelector('.chat-box');
if(chatBox){ chatBox.scrollTop = chatBox.scrollHeight; }
</script>
""", unsafe_allow_html=True)












