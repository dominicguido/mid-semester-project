import streamlit as st
import time


class StoreUI:

    def __init__(self, service, data) -> None:
        self.service = service
        self.data = data

    def apply_styles(self):
        st.markdown("""
        <style>
        .stApp {
            background: #0d1117;
        }

        .block-container {
            max-width: 1150px;
            padding-top: 1.8rem;
        }

        h1, h2, h3, h4, p, label {
            color: #f8fafc !important;
        }

        .info-card {
            background: linear-gradient(135deg, #ffffff, #f3f4f6);
            color: #111827;
            padding: 1.4rem;
            border-radius: 18px;
            margin-bottom: 1.3rem;
            box-shadow: 0 8px 22px rgba(0,0,0,0.25);
        }

        .info-card h3 {
            color: #111827 !important;
            margin-bottom: 0.25rem;
        }

        .info-card p {
            color: #1f2937 !important;
            margin: 0;
        }

        .product-card {
            background: #121820;
            padding: 1.2rem;
            border-radius: 16px;
            border: 1px solid #252c37;
            margin-bottom: 1rem;
        }

        .low-stock {
            color: #ff6b6b;
            font-weight: bold;
        }

        .good-stock {
            color: #51cf66;
            font-weight: bold;
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        textarea {
            background-color: #292c36 !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
        }

        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background-color: #292c36 !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
        }

        .stButton > button {
            height: 3rem;
            border-radius: 10px;
            font-weight: 700;
        }

        .stButton > button[kind="primary"] {
            background-color: #ff4b4b;
            border: none;
        }

        [data-testid="stMetric"] {
            background: #121820;
            padding: 1rem;
            border-radius: 14px;
            border: 1px solid #252c37;
        }
        </style>
        """, unsafe_allow_html=True)

    def login_page(self):
        self.apply_styles()

        st.title("📦 Small Business Inventory Manager")
        st.caption("Simple inventory tracking for owners and employees.")

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown("""
            <div class="info-card">
                <h3>↪ Log In</h3>
                <p>Enter your email and password to access your account.</p>
            </div>
            """, unsafe_allow_html=True)

            with st.container(border=True):
                st.subheader("Log In")

                email_input = st.text_input("Email", key="login_email")
                password_input = st.text_input("Password", type="password", key="login_password")

                if st.button("Log In", use_container_width=True, type="primary", key="login_button"):
                    with st.spinner("Logging in..."):
                        time.sleep(1)
                        user = self.service.login(email_input, password_input)

                    if user:
                        return user
                    else:
                        st.error("Invalid credentials")

        with col2:
            st.markdown("""
            <div class="info-card">
                <h3>👥 Create Account</h3>
                <p>Create a new account and choose your role.</p>
            </div>
            """, unsafe_allow_html=True)

            with st.container(border=True):
                st.subheader("New Account")

                new_email = st.text_input("Email Address", key="reg_email")
                new_password = st.text_input("Password", type="password", key="reg_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

                selected_role = st.selectbox(
                    "Role",
                    ["Select a role", "Employee", "Owner"]
                )

                if st.button("Create Account", use_container_width=True, type="primary", key="register_button"):
                    if not new_email or not new_password or not confirm_password:
                        st.warning("Please fill out all fields.")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match.")
                    elif selected_role == "Select a role":
                        st.warning("Please choose Employee or Owner.")
                    else:
                        with st.spinner("Creating account..."):
                            time.sleep(1)

                            try:
                                self.service.register(new_email, new_password, selected_role)
                            except TypeError:
                                self.service.register(new_email, new_password)

                        st.success("Account created")
                        time.sleep(1)
                        st.rerun()

        # ---------- Test Credentials ----------
        with st.container(border=True):
            st.markdown("### Test Credentials")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Owner Login**")
                st.write("Email: owner@business.com")
                st.write("Password: 123")

            with col2:
                st.markdown("**Employee Login**")
                st.write("Email: employee@business.com")
                st.write("Password: 456")

        return None

    def main(self):
        self.apply_styles()

        if st.session_state["role"] == "Owner":
            self.owner_dashboard()

        elif st.session_state["role"] == "Employee":
            self.employee_dashboard()

    def employee_dashboard(self):
        st.header("👷 Employee Dashboard")
        st.caption("View products and log daily sales.")

        inventory = self.service.all_inventory()

        total_products = len(inventory)
        total_stock = sum(item["stock"] for item in inventory)
        low_stock_count = sum(1 for item in inventory if item["stock"] <= 5)

        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("Total Products", total_products)
        metric2.metric("Total Items in Stock", total_stock)
        metric3.metric("Low Stock Items", low_stock_count)

        tab1, tab2 = st.tabs(["🛒 View Catalog", "🧾 Log Daily Sales"])

        with tab1:
            st.subheader("Current Catalog")

            if not inventory:
                st.warning("No products available")
            else:
                for item in inventory:
                    stock_status = "Low Stock" if item["stock"] <= 5 else "In Stock"
                    stock_class = "low-stock" if item["stock"] <= 5 else "good-stock"

                    st.markdown(f"""
                    <div class="product-card">
                        <h4>{item["name"]}</h4>
                        <p><strong>Category:</strong> {item.get("category", "Uncategorized")}</p>
                        <p>{item.get("description", "No description available.")}</p>
                        <p><strong>Price:</strong> ${float(item["price"]):.2f}</p>
                        <p><strong>Stock:</strong> {item["stock"]}
                        <span class="{stock_class}">({stock_status})</span></p>
                    </div>
                    """, unsafe_allow_html=True)

        with tab2:
            st.subheader("Log Daily Sales")

            if not inventory:
                st.warning("No products available")
            else:
                product_names = [item["name"] for item in inventory]

                col1, col2 = st.columns(2)

                with col1:
                    selected_product = st.selectbox("Select product sold", product_names)

                with col2:
                    quantity_sold = st.number_input("Quantity sold", min_value=1, value=1, step=1)

                if st.button("Log Sale", use_container_width=True, type="primary", key="log_sale_button"):
                    with st.spinner("Logging sale..."):
                        time.sleep(1)
                        result = self.service.log_sale(selected_product, quantity_sold)

                    if result:
                        st.success("Sale logged")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Not enough stock or invalid product")

    def owner_dashboard(self):
        st.header("👑 Owner Dashboard")
        st.caption("Manage products, inventory levels, prices, and discontinued items.")

        inventory = self.service.all_inventory()

        total_products = len(inventory)
        total_stock = sum(item["stock"] for item in inventory)
        low_stock_count = sum(1 for item in inventory if item["stock"] <= 5)

        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("Total Products", total_products)
        metric2.metric("Total Items in Stock", total_stock)
        metric3.metric("Low Stock Items", low_stock_count)

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 View Products",
            "➕ Add Product",
            "✏️ Update Product",
            "🗑️ Delete Product",
            "🤖 AI Assistant"
        ])

        with tab1:
            st.subheader("Product Inventory")

            if inventory:
                st.dataframe(inventory, use_container_width=True, hide_index=True)
            else:
                st.warning("No products available")

        with tab2:
            st.subheader("Add New Product")

            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Product Name", placeholder="ex. Water Bottle")
                stock = st.number_input("Stock Quantity", min_value=0, step=1)

            with col2:
                price = st.number_input("Price", min_value=0.0, step=0.01)

                category = st.selectbox(
                    "Category",
                    [
                        "Office Supplies",
                        "Food",
                        "Drinks",
                        "Electronics",
                        "Clothing",
                        "Health & Beauty",
                        "Home Goods",
                        "Other"
                    ]
                )

                description = st.text_area("Description", placeholder="ex. Reusable bottle...")

            if st.button("Save Product", use_container_width=True, type="primary", key="save_product_button"):
                if not name:
                    st.warning("Product name is required.")
                else:
                    with st.spinner("Saving product..."):
                        time.sleep(1)

                        try:
                            self.service.add_product(name, description, stock, price, category)
                        except TypeError:
                            self.service.add_product(name, description, stock, price)

                    st.success("Product saved")
                    time.sleep(1)
                    st.rerun()

        with tab3:
            st.subheader("Update Product")

            product_names = [item["name"] for item in inventory]

            if product_names:
                selected_product = st.selectbox("Select a product", product_names)

                selected_item = None
                for item in inventory:
                    if item["name"] == selected_product:
                        selected_item = item
                        break

                col1, col2 = st.columns(2)

                with col1:
                    new_price = st.number_input(
                        "Update Price",
                        min_value=0.0,
                        value=float(selected_item["price"]) if selected_item else 0.0,
                        step=0.01
                    )

                with col2:
                    new_stock = st.number_input(
                        "Restock Quantity",
                        min_value=0,
                        value=int(selected_item["stock"]) if selected_item else 0,
                        step=1
                    )

                if st.button("Update Product", use_container_width=True, type="primary", key="update_product_button"):
                    with st.spinner("Updating product..."):
                        time.sleep(1)
                        self.service.update_product(selected_product, new_price, new_stock)

                    st.success("Product updated")
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning("No products available")

        with tab4:
            st.subheader("Delete Product")

            if inventory:
                product_names = [item["name"] for item in inventory]
                selected_product = st.selectbox("Select product to delete", product_names)

                st.warning("Only delete products that are discontinued or no longer sold.")

                if st.button("Delete Product", use_container_width=True, type="primary", key="delete_product_button"):
                    with st.spinner("Deleting product..."):
                        time.sleep(1)
                        self.service.delete_product(selected_product)

                    st.success("Product deleted")
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning("No products available")

        with tab5:
            self.ai_assistant()

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