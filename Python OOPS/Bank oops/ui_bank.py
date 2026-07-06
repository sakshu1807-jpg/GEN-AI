import streamlit as st
from ai_bank import Bank  # Importing your engine

# Initialize the engine
# We use st.cache_resource so Streamlit doesn't reload the DB on every click
@st.cache_resource
def get_bank_instance():
    return Bank()

bank = get_bank_instance()

st.set_page_config(page_title="OOPS Bank", layout="centered")
st.title("🏦 Saksham National Bank")

tab1, tab2, tab3 = st.tabs(["Open Account", "Transactions", "Admin"])

with tab1:
    st.header("New Membership")
    with st.form("reg_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0)
        email = st.text_input("Email")
        pin = st.number_input("4-Digit PIN", min_value=1000, max_value=9999)
        if st.form_submit_button("Register"):
            success, result = bank.create_account(name, age, email, pin)
            if success:
                st.success(f"Success! Acc No: {result['Account_number']} created.")
            else:
                st.error(result)

with tab2:
    st.header("Banking Hub")
    auth_pin = st.number_input("Verify PIN", min_value=1000, max_value=9999, key="auth")
    action = st.radio("Action", ["Deposit", "Withdraw"])
    amt = st.number_input("Amount", min_value=0)
    
    if st.button("Execute Transaction"):
        # We pass a negative amount if it's a withdrawal
        actual_amount = amt if action == "Deposit" else -amt
        success, result = bank.update_balance(auth_pin, actual_amount)
        
        if success:
            st.success(f"Updated! New Balance: ${result}")
        else:
            st.error(result)

with tab3:
    st.header("System Logs")
    if st.checkbox("Show all accounts"):
        st.dataframe(bank.accounts)
