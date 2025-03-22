import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import random
import plotly.express as px

SHEET_URL = st.secrets["gcp_service_account"]["sheet_url"]

creds = None
if "gcp_service_account" in st.secrets:
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])

scope = [
    "https://spreadsheets.google.com/feeds", 
    "https://www.googleapis.com/auth/spreadsheets", 
    "https://www.googleapis.com/auth/drive.file", 
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/cloud-platform"
]

creds = creds.with_scopes(scopes=scope)

client = gspread.authorize(creds)
sheet = client.open_by_url(SHEET_URL).sheet1

st.title("💰 Expense Tracker")
st.header("📜 Expense Log")

data = sheet.get_all_records()
df = pd.DataFrame(data)

if not df.empty:
    st.write(df)
else:
    st.write("No expenses logged yet.")

st.header("📊 Current Debt Summary")

if not df.empty:
    debt_summary = df.pivot_table(
        values='Amount Spent',
        index='Name',
        columns='Paid By',
        aggfunc='sum',
        fill_value=0
    ).reset_index()
    
    debt_summary['Total'] = debt_summary.iloc[:, 1:].sum(axis=1)
    
    st.write(debt_summary)
    
    st.markdown("### 📈 Debt Distribution")
    
    debt_summary_sorted = debt_summary.sort_values('Total', ascending=True)
    
    colors = []
    for i in range(len(debt_summary_sorted)):
        intensity = i / len(debt_summary_sorted)
        color = f'rgb({255}, {192-intensity*192}, {203-intensity*203})'
        colors.append(color)
    colors.reverse()
    
    fig = px.pie(
        debt_summary_sorted,
        values='Total',
        names='Name',
        title='Total Debt Distribution',
        color_discrete_sequence=colors
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    highest_debtor = debt_summary.loc[debt_summary['Total'].idxmax()]["Name"]
    highest_amount = debt_summary['Total'].max()
    
    debt_messages = [
        f"Congratulations, {highest_debtor}! You've won the 'Best at Owing Money' award! Now, pay up before we start charging rent on your debt!",
        f"Breaking News: {highest_debtor} has officially been declared the CEO of Debt Inc. We wish them luck in their future bankruptcy!",
        f"Hey {highest_debtor}, NASA just called—they discovered a new black hole in your wallet! Pay your dues before we all get sucked in!",
        f"Debt Level: Final Boss Mode. {highest_debtor}, your financial decisions are now a horror story. Pay up before we make a documentary!",
        f"If money talks, yours has been on silent mode for too long, {highest_debtor}. Time to unmute those payments!",
        f"{highest_debtor}, you've borrowed so much, we're considering renaming this app after you. '{highest_debtor}'s Debt Tracker' has a nice ring to it, no?",
        f"Your debt is so high, even Elon Musk is impressed. Ready to clear it, or should we start crowdfunding your escape?"
    ]
    
    st.markdown(f"### 📢 Special Announcement for {highest_debtor}")
    st.write(random.choice(debt_messages))
else:
    st.write("No expenses logged yet.")

st.sidebar.header("🔑 Admin Login")
password = st.sidebar.text_input("Enter Admin Password", type="password")
ADMIN_PASSWORD = st.secrets["gcp_service_account"]["pwd"]

if password == ADMIN_PASSWORD:
    st.sidebar.success("✅ Admin Mode Activated!")

    st.header("📝 Log New Expense")
    name = st.text_input("Enter Your Name")
    amount = st.number_input("Amount Spent", min_value=0.0, format="%.2f")
    paid_by = st.text_input("Who Paid?")

    if st.button("Log Expense"):
        if name and amount > 0 and paid_by:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([name, amount, paid_by, timestamp])
            st.success("Expense Logged Successfully!")
            st.rerun()

    st.header("💵 Log a Payment")
    debtor_name = st.text_input("Enter Name Paying Off Debt")
    payment_amount = st.number_input("Amount Being Paid", min_value=0.0, format="%.2f")

    if st.button("Record Payment"):
        if debtor_name and payment_amount > 0:
            remaining_payment = payment_amount
            
            for index, row in df.iterrows():
                if row["Name"] == debtor_name and remaining_payment > 0:
                    if remaining_payment >= row["Amount Spent"]:
                        remaining_payment -= row["Amount Spent"]
                        sheet.delete_rows(index + 2)
                    else:
                        new_amount = row["Amount Spent"] - remaining_payment
                        sheet.update(f"B{index + 2}", [[new_amount]])
                        remaining_payment = 0

            st.success(f"✅ Payment of ₹{payment_amount} recorded for {debtor_name}!")
            st.rerun()

    st.sidebar.markdown("### 🔗 Google Sheets Access")
    st.sidebar.markdown(f"[📄 **View Full Sheet Here**]({SHEET_URL})")

if password == ADMIN_PASSWORD:
    st.write("🔍 **Check Google Sheets for full records!**")
    st.markdown(f"[📄 **View Full Sheet Here**]({SHEET_URL})")
