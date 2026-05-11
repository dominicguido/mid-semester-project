import streamlit as st
import json
from pathlib import Path
import uuid
import time

st.set_page_config(page_title="Inventory Manager", layout="centered")
st.title("Small Business Inventory Manager")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None
if "page" not in st.session_state:
    st.session_state["page"] = "login"

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
    {'id': '1', 'name': 'Notebook', 'description': 'College ruled notebooks', 'stock': 50, 'price': 4},
    {'id': '2', 'name': 'Pens', 'description': 'Blue ink pens pack', 'stock': 100, 'price': 2.5}
]

json_path_inventory = Path('inventory.json')
json_path_users = Path("users1.json")

if json_path_inventory.exists():
    with json_path_inventory.open('r', encoding='utf-8') as f:
        inventory = json.load(f)

if json_path_users.exists():
    with json_path_users.open('r', encoding='utf-8') as f:
        users1 = json.load(f)

if st.session_state['logged_in'] == False:
    st.subheader("Log In")
    email_input = st.text_input("Email", key="login_email")
    password_input = st.text_input("Password", type="password", key="login_password")

    if st.button("Log In", type='primary', use_container_width=True):
        with st.spinner("Logging in..."):
            time.sleep(1.5)
            found_user = None
            for user in users1:
                if user["email"].strip().lower() == email_input.strip().lower() and user["password"] == password_input:
                    found_user = user
                    break
            if found_user:
                st.session_state['logged_in'] = True
                st.session_state['user'] = found_user
                st.session_state['role'] = found_user['role']
                st.session_state['page'] = 'home'
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.subheader("New Account")
    new_email = st.text_input("Email Address", key="reg_email")
    new_password = st.text_input("Password", type="password", key="reg_password")

    if st.button("Create Account", type='secondary', use_container_width=True):
        with st.spinner("Creating account..."):
            time.sleep(1)
            users1.append({
                "id": str(uuid.uuid4()),
                "email": new_email,
                "password": new_password,
                "role": "Employee"
            })
            with open(json_path_users, "w") as f:
                json.dump(users1, f)
            st.success(f"Account created! {new_email}")
            time.sleep(1)
            st.rerun()
    
    

if st.session_state['logged_in'] == True:
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

    if st.session_state['role'] == 'Employee':
        st.markdown("### Employee Dashboard")
    
        tab1, tab2 = st.tabs(['View Catalog', 'Log Daily Sales'])

        with tab1:
            st.markdown("# Current Catalog")
            if not inventory:
                st.warning("No products available.")
            else:
                for item in inventory:
                    st.markdown(f"**{item['name']}** - Stock: {item['stock']}")
                    if item['stock'] <= 5:
                        st.error("Low stock!")

        with tab2:
            st.markdown("# Log Daily Sales")
            if not inventory:
                st.warning("No products available to log sales.")
            else:
                sold_names = [item['name'] for item in inventory]
                selected_sold_name = st.selectbox("Select product sold", sold_names)
                quantity_sold = st.number_input("Quantity sold", value=1, step=1)

                log_btn = st.button("Log Sale")
                if log_btn:
                    for item in inventory:
                        if item['name'] == selected_sold_name:
                            if quantity_sold > item['stock']:
                                st.error("Cannot sell more than current stock!")
                            else:
                                item['stock'] -= quantity_sold
                                with json_path_inventory.open('w', encoding='utf-8') as f:
                                    json.dump(inventory, f)
                                st.success(f"Logged sale of {quantity_sold} x {selected_sold_name}")
                            break

    elif st.session_state['role'] == 'Owner':
        if st.session_state["page"] == "home":
            st.markdown(f"Welcome {st.session_state['user']['email']}")
            if st.button('Go to Dashboard', type='primary', key='view_dash_btn'):
                st.session_state["page"] = 'dashboard'
                st.rerun()

        elif st.session_state["page"] == 'dashboard':
            tab1, tab2, tab3, tab4 = st.tabs([
                'View Products',
                'Add New Product',
                'Update Price / Restock',
                'Delete Discontinued Product'
            ])

            with tab1:
                st.dataframe(inventory)

            with tab2:
                name = st.text_input('Product Name', placeholder='ex. Water Bottle')
                description = st.text_area('Description', placeholder='ex. reusable bottle...')
                stock = st.number_input('Stock Quantity')
                price = st.number_input('Price')
                if st.button('Save Product', key='save_product'):
                    if name:
                        inventory.append({
                            'id': str(uuid.uuid4()),
                            'name': name,
                            'description': description,
                            'stock': stock,
                            'price': price
                        })
                        with json_path_inventory.open('w', encoding='utf-8') as f:
                            json.dump(inventory, f)
                        st.success("Product saved!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.warning("Product name is required")

            with tab3:
                product_names = [item['name'] for item in inventory]
                if product_names:
                    selected_name = st.selectbox("Select a product", product_names)
                    selected_item = next(item for item in inventory if item['name'] == selected_name)
                    new_price = st.number_input("Update Price", value=selected_item['price'])
                    new_stock = st.number_input("Restock Quantity", value=selected_item['stock'])
                    if st.button("Update Product", key='update_product'):
                        selected_item['price'] = new_price
                        selected_item['stock'] = new_stock
                        with json_path_inventory.open('w', encoding='utf-8') as f:
                            json.dump(inventory, f)
                        st.success("Product updated!")
                        time.sleep(1)
                        st.rerun()

            with tab4:
                if inventory:
                    product_names = [item['name'] for item in inventory]
                    selected_name = st.selectbox("Select a product to delete", product_names, key='delete_product')
                    if st.button("Delete Product", key='delete_product_btn'):
                        inventory = [item for item in inventory if item['name'] != selected_name]
                        with json_path_inventory.open('w', encoding='utf-8') as f:
                            json.dump(inventory, f)
                        st.success(f"{selected_name} deleted successfully!")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.warning("No products to delete")

                    