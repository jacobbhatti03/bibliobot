import streamlit as st

def require_google_login():
    """
    Enforce Google OAuth login using Streamlit OIDC.
    """
    if not getattr(st, "user", None) or not st.user.is_logged_in:
        st.info("Please sign in with Google to continue.")
        st.login("google")  # uses provider config from secrets.toml
        st.stop()

    return st.user


def sidebar_login_ui():
    with st.sidebar:
        if getattr(st, "user", None) and st.user.is_logged_in:
            st.write(f"Signed in as: **{st.user.email}**")
            if st.button("Logout"):
                st.logout()
                st.stop()
        else:
            st.caption("Not signed in")


