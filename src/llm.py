import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

def reply(prompt: str) -> str:
    model = get_model()
    if model is None:
        return "⚠️ GEMINI_API_KEY not found. Add it to your environment/secrets."
    res = model.generate_content(prompt)
    return getattr(res, "text", "") or ""
