import streamlit as st
from pathlib import Path
import time


from data.store_data import StoreData
from service.store_service import StoreService
from ui.store_ui import StoreUI


st.set_page_config(page_title="Inventory Manager")

st.title("Small Business Inventory Manager")


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"


store_data = StoreData(
    Path("users1.json"),
    Path("inventory.json")
)

service = StoreService(store_data)
ui = StoreUI(service, store_data)


if st.session_state["logged_in"]:
    with st.sidebar:
            st.markdown(f"### Logged in as: {st.session_state['user']['email']}")
            if st.button("Log Out"):
                with st.spinner("Logging out..."):
                    time.sleep(1)
                    st.session_state['logged_in'] = False
                    st.session_state['user'] = None
                    st.session_state['role'] = None
                    st.session_state['page'] = 'login'
                    st.rerun()

    ui.main()


else:

    user = ui.login_page()

    if user:

        st.session_state["logged_in"] = True
        st.session_state["user"] = user
        st.session_state["role"] = user["role"]

        st.session_state["page"] = "home"

        st.rerun()

    st.markdown("### Test Logins")
    st.markdown(
    'Owner Login: Email: owner@business.com, Password: 123')
    
    st.markdown('Employee Login: Email: employee@business.com, Password: 456')


