import streamlit as st
from pathlib import Path

from refactored_code.data.store_data import StoreData
from refactored_code.service.store_service import StoreService
from refactored_code.ui.store_ui import StoreUI


# ---------- Session State ----------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"


# ---------- Initialize Classes ----------
data = StoreData(
    Path("users1.json"),
    Path("inventory.json")
)

service = StoreService(data)

ui = StoreUI(service, data)


# ---------- App ----------
if not st.session_state["logged_in"]:

    user = ui.login_page()

    if user:
        st.session_state["logged_in"] = True
        st.session_state["user"] = user
        st.session_state["role"] = user["role"]
        st.session_state["page"] = "home"
        st.rerun()

else:

    with st.sidebar:
        st.header("Account")

        st.write(f"**Email:** {st.session_state['user']['email']}")
        st.write(f"**Role:** {st.session_state['role']}")

        if st.button("Log Out", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.session_state["page"] = "login"
            st.rerun()

    ui.main()