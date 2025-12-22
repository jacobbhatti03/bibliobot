import streamlit as st

def get_user():
    # Skeleton mode: no login required yet
    return None

def sidebar_login_ui():
    with st.sidebar:
        st.caption("Auth: disabled (skeleton mode)")
