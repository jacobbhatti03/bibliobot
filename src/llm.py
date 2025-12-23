import os
import streamlit as st
import google.generativeai as genai

MODEL_NAME = "gemini-2.5-flash"

def _get_api_key() -> str | None:
    # Streamlit Cloud secrets first
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]

    # Local fallback (if you set it in environment variables)
    return os.getenv("GEMINI_API_KEY")

def get_model():
    api_key = _get_api_key()
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL_NAME)

def reply(prompt: str) -> str:
    model = get_model()
    if model is None:
        return "⚠️ GEMINI_API_KEY missing. Add it in Streamlit Secrets (GEMINI_API_KEY)."
    res = model.generate_content(prompt)
    return getattr(res, "text", "") or ""

