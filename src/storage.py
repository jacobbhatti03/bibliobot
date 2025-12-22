import streamlit as st

def init_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def add(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})

def clear():
    st.session_state.messages = []
