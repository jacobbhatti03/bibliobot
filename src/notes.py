import streamlit as st

def _key(user_id: str):
    return f"notes_{user_id}"

def get_notes(user_id: str):
    return st.session_state.get(_key(user_id), [])

def add_note(user_id: str, title: str, content: str):
    notes = get_notes(user_id)
    notes.append({"title": (title or "Note").strip()[:80], "content": content.strip()})
    st.session_state[_key(user_id)] = notes

def format_notes_for_prompt(user_id: str) -> str:
    notes = get_notes(user_id)
    if not notes:
        return ""
    recent = notes[-5:]
    out = ["User Scripture Notes (recent):"]
    for n in recent:
        out.append(f"- {n['title']}: {n['content'][:300]}")
    return "\n".join(out)


