import streamlit as st
import time


class StoreUI:

    def __init__(self, service, data) -> None:
        self.service = service
        self.data = data

    def ai_assistant(self):

        st.subheader("AI Inventory Assistant")

        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {
                    "role": "assistant",
                    "content": "Hi! Ask me anything about your inventory."
                }
            ]

        with st.container(height=300, border=True):

            for message in st.session_state["messages"]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        user_input = st.chat_input("Ask a question...")

        if user_input:

            st.session_state["messages"].append({
                "role": "user",
                "content": user_input
            })

            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    time.sleep(1)
                    response = self.service.ask_ai(st.session_state["messages"])

                st.markdown(response)

            st.session_state["messages"].append({
                "role": "assistant",
                "content": response
            })

    def main(self):

        if st.session_state["role"] == "Owner":
            self.owner_dashboard()

        elif st.session_state["role"] == "Employee":
            self.employee_dashboard()

    def login_page(self):

        st.subheader("Log In")

        email_input = st.text_input("Email", key='login_email')
        password_input = st.text_input("Password", type="password", key='login_password')

        if st.button("Log In", use_container_width=True, type='primary'):
            with st.spinner("Logging in..."):
                time.sleep(2)
                user = self.service.login(email_input, password_input)

                if user:
                    return user
                else:
                    st.error("Invalid credentials")

        st.subheader("New Account")

        new_email = st.text_input("Email Address", key='reg_email')
        new_password = st.text_input("Password", type="password", key='reg_password')

        if st.button("Create Account", use_container_width=True, type='primary'):
            with st.spinner("Creating account..."):
                time.sleep(2)
                st.success("Account created")
                users = self.data.load_users()

                self.service.register(new_email, new_password)

                st.success("Account created")
                st.rerun()

        return None

    def employee_dashboard(self):

        st.subheader("Employee Dashboard")

        tab1, tab2 = st.tabs(["View Catalog", "Log Daily Sales"])

        inventory = self.service.all_inventory()

        with tab1:

            st.markdown("Current Catalog")

            if not inventory:
                st.warning("No products available")

            else:
                for item in inventory:
                    st.markdown("**" + item["name"] + "** - Stock: " + str(item["stock"]))

                    if item["stock"] <= 5:
                        st.error("Low stock!")

        with tab2:

            st.markdown("Log Daily Sales")

            if not inventory:
                st.warning("No products available")

            else:

                product_names = []

                for item in inventory:
                    product_names.append(item["name"])

                selected_product = st.selectbox("Select product sold", product_names)

                quantity_sold = st.number_input("Quantity sold", value=1, step=1)

                if st.button("Log Sale", use_container_width=True, type='primary'):
                    with st.spinner("Logging sale..."):
                        time.sleep(2)
                        

                    result = self.service.log_sale(selected_product, quantity_sold)

                    if result:
                        st.success("Sale logged")

                    else:
                        st.error("Not enough stock or invalid product")

    def owner_dashboard(self):

        st.subheader("Owner Dashboard")

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "View Products",
            "Add Product",
            "Update Product",
            "Delete Product",
            'AI Assistant'
        ])

        inventory = self.service.all_inventory()

        with tab1:

            for item in inventory:
                st.markdown("**" + item["name"] + "** | Stock: " + str(item["stock"]) + " | Price: " + str(item["price"]))

        with tab2:

            name = st.text_input("Product Name")
            description = st.text_area("Description")
            stock = st.number_input("Stock Quantity")
            price = st.number_input("Price")

            if st.button("Save Product", use_container_width=True, type='primary'):
                with st.spinner("Saving product..."):
                    time.sleep(2)
                    self.service.add_product(name, description, stock, price)

                st.success("Product saved")
                time.sleep(2)
                st.rerun()

        with tab3:

            product_names = []

            for item in inventory:
                product_names.append(item["name"])

            selected_product = st.selectbox("Select a product", product_names)

            new_price = st.number_input("Update Price")
            new_stock = st.number_input("Restock Quantity")

            if st.button("Update Product",  use_container_width=True, type='primary'):
                with st.spinner("Updating product..."):
                    time.sleep(2)
                    self.service.update_product(selected_product, new_price, new_stock)

                st.success("Product updated")
                time.sleep(2)
                st.rerun()

        with tab4:

            if inventory:

                product_names = []

                for item in inventory:
                    product_names.append(item["name"])

                selected_product = st.selectbox("Select product to delete", product_names)

                if st.button("Delete Product",  use_container_width=True, type='primary'):
                    with st.spinner("Deleting product..."):
                        time.sleep(2)
                    self.service.delete_product(selected_product)

                    st.success("Product deleted")
                    time.sleep(2)
                    st.rerun()

            else:
                st.warning("No products available")
            
        with tab5:
            self.ai_assistant()

   