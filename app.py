import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config(page_title="Inventory Manager", layout="centered")
st.title("Small Business Inventory Manager")


# Initialize Session State
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None 

if "page" not in st.session_state:
    st.session_state["page"] = "login" or "register"



users1 = [
    {
    "id": "1",
    "email": "owner@business.com",
    "full_name": "Business Owner",
    "password": "123",
    "role": "Owner"
}
]

inventory = [
    {
        'id': 'ITEM1',
        'name': 'Notebook',
        'description': 'College ruled notebooks',
        'stock': 50,
        'category': 'Office Supplies'
    },
    {
        'id': 'ITEM2',
        'name': 'Pens',
        'description': 'Blue ink pens pack',
        'stock': 100,
        'category': 'Office Supplies'
    }
]

json_path_inventory = Path('inventory.json')

# load the data from a json file
if json_path_inventory.exists(): 
    with json_path_inventory.open('r', encoding='utf-8') as f:
        inventory = json.load(f)


json_path = Path("users1.json")

if json_path.exists():
    with open(json_path, "r") as f:
        users1 = json.load(f)

if st.session_state['role'] == 'Owner':
    st.markdown('This is the Owner UI - Dashboard')

    if st.button('Log Out'):
        with st.spinner('Logging Out'):
            time.sleep(3)
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.rerun()



elif st.session_state['role'] == 'Employee':
    if st.session_state["page"] == "home":
        st.markdown(f"Welcome {st.session_state['user']['email']}")
        if st.button('Go to Dashboard', type='primary', key='view_dash_btn'):
            st.session_state["page"] = 'dashboard'
            st.rerun()

    elif st.session_state["page"] == 'dashboard':
        tab1, tab2, tab3 = st.tabs(['View Inventory', 'Add New Item', 'Update an Item'])

        with tab1:
            tab_option = st.radio('View/Search', ['View', 'Search'], horizontal=True)

            if tab_option == 'View':
                st.dataframe(inventory)

            else:
                names = []
                for item in inventory:
                    names.append(item['name'])
                
                if not names:
                    st.warning('No inventory item found')
                else:
                    selected_name = st.selectbox('Item Name', names)

                for item in inventory:
                    if item['name'] == selected_name:
                        with st.expander('Item Details', expanded=True):
                            st.markdown(f"### Name: {item['name']}")
                            st.markdown(f"Description: {item['description']}")
                            st.markdown(f"Category: **{item['category']}**")
                            st.markdown(f"Stock: **{item['stock']}**")
                            break

        with tab2:
            st.markdown('# Add New Inventory Item')

            with st.container(border=True):
                name = st.text_input('Item Name', placeholder='ex. Water Bottle')
                description = st.text_area('Description', placeholder='ex. reusable bottles...')
                stock = st.number_input('Stock Quantity')
                restock_date = st.date_input('Restock Date')

                category = st.selectbox('Category', ['Office Supplies', 'Electronics', 'Food', 'Other'])
                if category == 'Other':
                    category = st.text_input('Item Category')

                st.markdown('#### Live Preview')
                st.markdown(f"Item: {name}")

            btn_save = st.button('Save', width='stretch', disabled=False)

            if btn_save:
                if not name:
                    st.warning('Item name needs to be provided')
                else:
                    with st.spinner('Item is being recorded...'):
                        time.sleep(3)

                        inventory.append(
                            {
                                'id': str(uuid.uuid4()),
                                'name': name,
                                'description': description,
                                'stock': stock,
                                'category': category
                            }
                        )

                        with json_path_inventory.open('w', encoding='utf-8') as f:
                            json.dump(inventory, f)

                    st.success('New inventory item recorded!')
                    st.dataframe(inventory)


        with tab3:
            st.markdown("# Update an Inventory Item")
            names = []

            for item in inventory:
                names.append(item["name"])

            selected_item_name = st.selectbox("Select an item", names, key='search_items')

            selected_inventory = {}
            for item in inventory:
                if item["name"] == selected_item_name:
                    selected_inventory = item
                    break

            edit_name = st.text_input(
                'Item Name',
                value=selected_inventory['name'],
                key=f"edit_name{selected_inventory['name']}"
            )

            edit_description = st.text_area(
                'Description',
                value=selected_inventory['description'],
                key=f"edit_description{selected_inventory['description']}"
            )

            category_list = ['Office Supplies', 'Electronics', 'Food']
            selected_category_index = category_list.index(selected_inventory['category']) if selected_inventory['category'] in category_list else 0

            edit_category = st.radio(
                'Category',
                category_list,
                index=selected_category_index,
                key=f"edit_category{selected_inventory['id']}"
            )

            update_btn = st.button(
                'Update Item',
                key='btn_update',
                use_container_width=True,
                type='primary'
            )

            if update_btn:
                with st.spinner('Updating the item'):
                    time.sleep(3)
                    selected_inventory['name'] = edit_name
                    selected_inventory['description'] = edit_description
                    selected_inventory['category'] = edit_category

                    with json_path_inventory.open('w', encoding='utf-8') as f:
                        json.dump(inventory, f)

                    st.success('Inventory item updated!')
                    time.sleep(3)
                    st.rerun()

else:
    st.subheader("Log In")
    with st.container(border=True):
        email_input = st.text_input("Email", key="login_email")
        password_input = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Log In", type='primary', use_container_width=True):
            with st.spinner("Logging in..."):
                time.sleep(2)
                
                found_user = None
                for user in users1:
                    if user["email"].strip().lower() == email_input.strip().lower() and user["password"] == password_input:
                        found_user = user
                        break
                
                if found_user:
                    st.success(f"Welcome back, {found_user['email']}!")
                    st.session_state['logged_in'] = True
                    st.session_state["user"] = found_user
                    st.session_state["role"] = found_user["role"]
                    st.session_state["page"] = "home"
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Invalid credentials")



    st.subheader("New Employee Account")
    with st.container(border=True):
        new_email = st.text_input("Email Address", key="reg_email")
        new_password = st.text_input("Password", type="password", key="reg_password")
        
        if st.button("Create Account", type='secondary', use_container_width=True):
            with st.spinner("Creating account..."):
                time.sleep(2)

                users1.append({
                    "id": str(uuid.uuid4()),
                    "email": new_email,
                    "password": new_password,
                    "role": "Employee"
                })

                with open(json_path, "w") as f:
                    json.dump(users1, f, indent=4)

                st.success(f"Account created! {new_email}")
                time.sleep(4)
                st.rerun()

    st.write("---")
    st.dataframe(users1)