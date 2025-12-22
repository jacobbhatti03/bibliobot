import streamlit as st

def _key(user_id: str | None):
    return f"messages_{user_id}" if user_id else "messages_guest"

def init_chat(user_id: str | None = None):
    key = _key(user_id)
    if key not in st.session_state:
        st.session_state[key] = []

def add(role: str, content: str, user_id: str | None = None):
    st.session_state[_key(user_id)].append({
        "role": role,
        "content": content
    })

def get(user_id: str | None = None):
    return st.session_state.get(_key(user_id), [])

def clear(user_id: str | None = None):
    st.session_state[_key(user_id)] = []
