import streamlit as st
from src.storage import clear

st.header("⚙️ Settings")

if st.button("Clear chat history"):
    clear()
    st.success("Chat history cleared.")
