import streamlit as st
from src.constants import APP_NAME, APP_TAGLINE

def header():
    st.title(APP_NAME)
    st.caption(APP_TAGLINE)
