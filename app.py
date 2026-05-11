import streamlit as st
import json
from pathlib import Path
import uuid
import time

st.set_page_config(page_title="Inventory Manager", layout="wide")

# ---------- Styling ----------
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

.app-subtitle {
    color: #9ca3af !important;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
}

.info-card {
    background: linear-gradient(135deg, #ffffff, #f3f4f6);
    color: #111827;
    padding: 1.4rem;
    border-radius: 18px;
    margin-bottom: 1.3rem;
    box-shadow: 0 8px 22px rgba(0,0,0,0.25);
    min-height: 115px;
}

.info-card h3 {
    color: #111827 !important;
    margin-bottom: 0.25rem;
}

.info-card p {
    color: #1f2937 !important;
    margin: 0;
}

.panel {
    background: linear-gradient(145deg, #121820, #0d1117);
    padding: 2rem;
    border-radius: 18px;
    border: 1px solid #252c37;
    box-shadow: 0 8px 25px rgba(0,0,0,0.28);
    min-height: 470px;
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

[data-testid="stSidebar"] {
    background: #111827;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.title("📦 Small Business Inventory Manager")
st.markdown('<p class="app-subtitle">Simple inventory tracking for owners and employees.</p>', unsafe_allow_html=True)

# ---------- Data ----------
json_path_inventory = Path("inventory.json")
json_path_users = Path("users1.json")

inventory = [
    {"id": "1", "name": "Notebook", "description": "College ruled notebooks", "stock": 50, "price": 4},
    {"id": "2", "name": "Pens", "description": "Blue ink pens pack", "stock": 100, "price": 2.5},
]

users1 = [
    {
        "id": "1",
        "email": "owner@business.com",
        "full_name": "Business Owner",
        "password": "123",
        "role": "Owner",
    }
]

if json_path_inventory.exists():
    with json_path_inventory.open("r", encoding="utf-8") as f:
        inventory = json.load(f)

if json_path_users.exists():
    with json_path_users.open("r", encoding="utf-8") as f:
        users1 = json.load(f)

# ---------- Session State ----------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"


def save_inventory():
    with json_path_inventory.open("w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=4)


def save_users():
    with json_path_users.open("w", encoding="utf-8") as f:
        json.dump(users1, f, indent=4)


# ---------- Login / Register ----------
if not st.session_state["logged_in"]:
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>ⓘ &nbsp; Log In</h3>
            <p>Enter your email and password to access your account.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            st.subheader("↪ Log In")

            email_input = st.text_input("Email", placeholder="Enter your email", key="login_email")
            password_input = st.text_input("Password", placeholder="Enter your password", type="password", key="login_password")
            remember_me = st.checkbox("Remember me")

            if st.button("Log In", type="primary", use_container_width=True):
                found_user = None

                for user in users1:
                    if user["email"].strip().lower() == email_input.strip().lower() and user["password"] == password_input:
                        found_user = user
                        break

                if found_user:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = found_user
                    st.session_state["role"] = found_user["role"]
                    st.session_state["page"] = "home"
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>👥 &nbsp; Create Account</h3>
            <p>Create a new account and choose your role.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            st.subheader("👥 Create Account")

            new_email = st.text_input("Email Address", placeholder="Enter email address", key="reg_email")
            new_password = st.text_input("Password", placeholder="Enter password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", placeholder="Confirm password", type="password", key="confirm_password")

            selected_role = st.selectbox(
                "Role",
                ["Select a role", "Employee", "Owner"],
                help="Choose whether this account will have Employee or Owner access."
            )

            st.caption("Choose whether this account will have Employee or Owner access.")

            if st.button("Create Account", use_container_width=True):
                existing_email = any(user["email"].strip().lower() == new_email.strip().lower() for user in users1)

                if not new_email or not new_password or not confirm_password:
                    st.warning("Please fill out all fields.")
                elif existing_email:
                    st.error("An account with this email already exists.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                elif selected_role == "Select a role":
                    st.warning("Please choose Employee or Owner.")
                else:
                    users1.append({
                        "id": str(uuid.uuid4()),
                        "email": new_email,
                        "full_name": new_email.split("@")[0],
                        "password": new_password,
                        "role": selected_role,
                    })
                    save_users()
                    st.success(f"{selected_role} account created for {new_email}.")
                    time.sleep(1)
                    st.rerun()
        # ---------- Test Credentials ----------
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        <div style="
            background: #121820;
            border: 1px solid #252c37;
            border-radius: 12px;
            padding: 0.9rem 1rem;
            text-align: center;
            color: #d1d5db;
            font-size: 0.9rem;
            margin-top: 2rem;
        ">
            <strong style="color:white;">Test Credentials</strong><br><br>
            <strong>Owner</strong><br>
            Email: owner@business.com<br>
            Password: 123<br><br>
            <strong>Employee</strong><br>
            Email: employee@business.com<br>
            Password: 456
        </div>
        """, unsafe_allow_html=True)    

# ---------- Logged In Area ----------
if st.session_state["logged_in"]:
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

    total_products = len(inventory)
    total_stock = sum(item["stock"] for item in inventory)
    low_stock_count = sum(1 for item in inventory if item["stock"] <= 5)

    # ---------- Employee Dashboard ----------
    if st.session_state["role"] == "Employee":
        st.header("👷 Employee Dashboard")
        st.caption("View products and log daily sales.")

        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("Total Products", total_products)
        metric2.metric("Total Items in Stock", total_stock)
        metric3.metric("Low Stock Items", low_stock_count)

        tab1, tab2 = st.tabs(["🛒 View Catalog", "🧾 Log Daily Sales"])

        with tab1:
            st.subheader("Current Catalog")

            if not inventory:
                st.warning("No products available.")
            else:
                for item in inventory:
                    stock_status = "Low Stock" if item["stock"] <= 5 else "In Stock"
                    stock_class = "low-stock" if item["stock"] <= 5 else "good-stock"

                    st.markdown(f"""
                    <div class="product-card">
                        <h4>{item['name']}</h4>
                        <p>{item.get('description', 'No description available.')}</p>
                        <p><strong>Price:</strong> ${item['price']:.2f}</p>
                        <p><strong>Stock:</strong> {item['stock']} 
                        <span class="{stock_class}">({stock_status})</span></p>
                    </div>
                    """, unsafe_allow_html=True)

        with tab2:
            st.subheader("Log a Sale")

            if not inventory:
                st.warning("No products available to log sales.")
            else:
                col1, col2 = st.columns(2)

                with col1:
                    sold_names = [item["name"] for item in inventory]
                    selected_sold_name = st.selectbox("Select Product Sold", sold_names)

                with col2:
                    quantity_sold = st.number_input("Quantity Sold", min_value=1, value=1, step=1)

                if st.button("Log Sale", type="primary", use_container_width=True):
                    for item in inventory:
                        if item["name"] == selected_sold_name:
                            if quantity_sold > item["stock"]:
                                st.error("Cannot sell more than current stock.")
                            else:
                                item["stock"] -= quantity_sold
                                save_inventory()
                                st.success(f"Logged sale of {quantity_sold} x {selected_sold_name}.")
                                time.sleep(1)
                                st.rerun()

    # ---------- Owner Dashboard ----------
    elif st.session_state["role"] == "Owner":
        st.header("👑 Owner Dashboard")
        st.caption("Manage products, inventory levels, prices, and discontinued items.")

        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("Total Products", total_products)
        metric2.metric("Total Items in Stock", total_stock)
        metric3.metric("Low Stock Items", low_stock_count)

        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 View Products",
            "➕ Add Product",
            "✏️ Update Product",
            "🗑️ Delete Product"
        ])

        with tab1:
            st.subheader("Product Inventory")

            if inventory:
                st.dataframe(inventory, use_container_width=True, hide_index=True)
            else:
                st.warning("No products found.")

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

                description = st.text_area(
                    "Description",
                    placeholder="ex. Reusable bottle..."
                )

            if st.button("Save Product", type="primary", use_container_width=True):
                if name:
                    inventory.append({
                        "id": str(uuid.uuid4()),
                        "name": name,
                        "description": description,
                        "stock": stock,
                        "price": price,
                    })
                    save_inventory()
                    st.success("Product saved.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("Product name is required.")

        with tab3:
            st.subheader("Update Price or Stock")

            product_names = [item["name"] for item in inventory]

            if product_names:
                selected_name = st.selectbox("Select Product", product_names)
                selected_item = next(item for item in inventory if item["name"] == selected_name)

                col1, col2 = st.columns(2)

                with col1:
                    new_price = st.number_input("Update Price", value=float(selected_item["price"]), min_value=0.0, step=0.01)

                with col2:
                    new_stock = st.number_input("Update Stock", value=int(selected_item["stock"]), min_value=0, step=1)

                if st.button("Update Product", type="primary", use_container_width=True):
                    selected_item["price"] = new_price
                    selected_item["stock"] = new_stock
                    save_inventory()
                    st.success("Product updated.")
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning("No products available to update.")

        with tab4:
            st.subheader("Delete Discontinued Product")

            if inventory:
                product_names = [item["name"] for item in inventory]
                selected_name = st.selectbox("Select Product to Delete", product_names, key="delete_product")

                st.warning("Only delete products that are discontinued or no longer sold.")

                if st.button("Delete Product", type="primary", use_container_width=True):
                    inventory = [item for item in inventory if item["name"] != selected_name]
                    save_inventory()
                    st.success(f"{selected_name} deleted successfully.")
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning("No products to delete.")  