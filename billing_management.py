import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Google Sheets Setup
SHEET_URL = st.secrets["gcp_service_account"]["sheet_url"]

# Load credentials from Streamlit secrets
creds = None
if "gcp_service_account" in st.secrets:
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])

# Google Sheets API Setup
scope = [
    "https://spreadsheets.google.com/feeds", 
    "https://www.googleapis.com/auth/spreadsheets", 
    "https://www.googleapis.com/auth/drive.file", 
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/cloud-platform"
]

creds = creds.with_scopes(scopes=scope)

# Authenticate and connect to Google Sheets
client = gspread.authorize(creds)
sheet = client.open_by_url(SHEET_URL).sheet1

# Streamlit UI
st.title("💰 Expense Tracker")

# **Show Only Log by Default**
st.header("📜 Expense Log")

# Fetch all data from Google Sheets
data = sheet.get_all_records()
df = pd.DataFrame(data)

if not df.empty:
    st.write(df)
else:
    st.write("No expenses logged yet.")

# **Admin Login**
st.sidebar.header("🔑 Admin Login")
password = st.sidebar.text_input("Enter Admin Password", type="password")
ADMIN_PASSWORD = "123" 

if password == ADMIN_PASSWORD:
    st.sidebar.success("✅ Admin Mode Activated!")

    # **Logging Expenses**
    st.header("📝 Log New Expense")
    name = st.text_input("Enter Your Name")
    amount = st.number_input("Amount Spent", min_value=0.0, format="%.2f")
    paid_by = st.text_input("Who Paid?")

    if st.button("Log Expense"):
        if name and amount > 0 and paid_by:
            sheet.append_row([name, amount, paid_by])
            st.success("Expense Logged Successfully!")
            st.rerun()

    # **Display Debt Summary**
    st.header("📊 Current Debt Summary")

    if not df.empty:
        debt_summary = df.groupby("Name")["Amount Spent"].sum().reset_index()
        st.write(debt_summary)
    else:
        st.write("No expenses logged yet.")

    # **Paying Off Debts**
    st.header("💵 Log a Payment")
    debtor_name = st.text_input("Enter Name Paying Off Debt")
    payment_amount = st.number_input("Amount Being Paid", min_value=0.0, format="%.2f")

    if st.button("Record Payment"):
        if debtor_name and payment_amount > 0:
            remaining_payment = payment_amount

            # Process payments in order
            for index, row in df.iterrows():
                if row["Name"] == debtor_name and remaining_payment > 0:
                    if remaining_payment >= row["Amount Spent"]:
                        remaining_payment -= row["Amount Spent"]
                        sheet.delete_rows(index + 2)  # Delete row after full payment
                    else:
                        new_amount = row["Amount Spent"] - remaining_payment
                        sheet.update(f"B{index + 2}", [[new_amount]])  # Update remaining debt
                        remaining_payment = 0

            st.success(f"✅ Payment of ₹{payment_amount} recorded for {debtor_name}!")
            st.rerun()

    # **Hide Google Sheets Link Behind Admin Login**
    st.sidebar.markdown("### 🔗 Google Sheets Access")
    st.sidebar.markdown(f"[📄 **View Full Sheet Here**]({SHEET_URL})")

# Footer (Hidden if not admin)
if password == ADMIN_PASSWORD:
    st.write("🔍 **Check Google Sheets for full records!**")
    st.markdown(f"[📄 **View Full Sheet Here**]({SHEET_URL})")
