import streamlit as st
from Shop_management_system import Shop 
from datetime import date, time

# Page Config
st.set_page_config(page_title="MANAGEMENT SYSTEM", layout="wide")
st.title("🛒 NM ENTERPRISES")

# Initialize Engine
@st.cache_resource
def init_shop():
    return Shop()

shop = init_shop()

# Sidebar Navigation
menu = ["Add Customer", "Update Balance", "All Customer Records", "View Customer History", "Delete Customer Record"]
choice = st.sidebar.selectbox("Action Center", menu)

if choice == "Add Customer":
    st.subheader("New Customer Entry")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Customer Name")
        balance = st.number_input("Initial Balance (₹)", min_value=0)
    with col2:
        items = st.text_area("Items (comma separated)").split(",")
        today_date = st.date_input("Purchase Date", date.today())
        time_today = st.time_input("Purchase Time", 'now')
    
    if st.button("Add Customer"):
        if name:
            shop.create_customer_info(name, balance, [i.strip() for i in items], str(today_date), str(time_today))
            st.success(f"Record created for {name}!")
        else:
            st.error("Name is required.")

elif choice == "Update Balance":
    st.subheader("Existing Customer Update")
    search_name = st.text_input("Enter Customer Name to find")
    
    # We use a button to trigger the search
    if search_name:
        customer = shop.find_customer(search_name)
        if isinstance(customer, dict): # Check if we actually got a dictionary (the customer)
            st.info(f"Current Balance: ₹{customer['customer_balance']}")
            new_val = st.number_input("Add to Balance", value=0)
            new_items = st.text_input("Add New Items (comma separated)").split(",")
            
            if st.button("Add Changes"):
                shop.update_record(search_name, new_val, [i.strip() for i in new_items if i])
                st.success("Record updated!")
                st.rerun() # Refresh to show new data
        else:
            st.warning("Customer not found.")

elif choice == "All Customer Records":
    st.subheader("All Customer Records")
    all_customers = shop.customer_list() 
    if all_customers:
        st.table(all_customers)
    else:
        st.write("No records found.")

elif choice == "View Customer History":
    st.subheader("📜 Customer Transaction History")
    search_name = st.text_input("Enter Customer Name to find")
    if search_name:
        customer = shop.find_customer(search_name)

        col1, col2 = st.columns(2)
        col1.metric("Current Balance", f"₹{customer['customer_balance']}")
        col2.metric("Total Items Bought", len(customer['items_purchased']))
        
        st.divider()
        
        if 'history' in customer and customer['history']:
            st.write("### Transaction Log")
            # We convert the list of dicts into a table
            st.table(customer['history'])
        else:
            st.info("No transaction history found for this user.")

elif choice == "Delete Customer Record":
    st.subheader("Danger Zone")
    del_name = st.text_input("Name to Delete")
    if st.button("Delete Customer Permanently"):
        success = shop.remove_customer(del_name)
        if success:
            st.warning(f"Deleted {del_name}")