import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Gandra Wealth Command", layout="wide")
st.title("🛡️ Gandra Household Wealth Command Center")

# --- 1. Connect to Data ---
conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1UDG5_ouvwhEMFAxBrhIFczRKU0jtbkpidiU0phkCdQg/edit?usp=sharing" # Put your sheet's share URL here

# Load Tabs
rsu_df = conn.read(spreadsheet=url, worksheet="RSU_Lots")
retire_df = conn.read(spreadsheet=url, worksheet="Retirement_Tracker")
bonus_df = conn.read(spreadsheet=url, worksheet="Income_Bonus")

# --- 2. Real-Time Calculations ---
wmt_price = 133.89 # We can automate this with yfinance later
total_wmt_value = rsu_df[rsu_df['Status'] == 'Vested']['Shares'].sum() * wmt_price
current_401k = retire_df[retire_df['Account_Type'] == '401k']['Amount'].sum()
roth_ira_total = retire_df[retire_df['Account_Type'] == 'Roth IRA']['Amount'].sum()

# --- 3. Dashboard Layout ---
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("WMT Stock Equity", f"${total_wmt_value:,.2f}")
kpi2.metric("2026 401(k) Progress", f"${current_401k:,.0f}", f"of $24,500 limit")
kpi3.metric("Roth IRA (Backdoor)", f"${roth_ira_total:,.0f}", "Limit: $15,000")

st.divider()

# --- 4. Strategy Tabs ---
tab1, tab2, tab3 = st.tabs(["📉 RSU Sell Schedule", "💰 Bonus Tax Shield", "📅 Task Reminders"])

with tab1:
    st.subheader("Vested Lots Available for Diversification")
    # Highlight Long-Term lots in Green for the user
    rsu_df['Action'] = rsu_df['Holding_Type'].apply(lambda x: "✅ READY TO SELL" if x == 'Long-Term' else "⏳ WAIT")
    st.dataframe(rsu_df.sort_values('Holding_Type', ascending=False))
    st.warning("Next Action: March 10th Vest - SELL IMMEDIATELY (Est. $27,323)")

with tab2:
    st.subheader("March 2026 Bonus Optimization")
    bonus_amt = 28600
    shield_amt = bonus_amt * 0.50
    st.write(f"Sandeep's Bonus: **${bonus_amt:,.0f}**")
    st.info(f"Strategy: Shield **${shield_amt:,.0f}** in Traditional 401(k) to save ~$4,290 in taxes.")
    
with tab3:
    st.subheader("Action Items")
    st.checkbox("Tuesday: Execute 107-share WMT sale")
    st.checkbox("March 11: Execute Backdoor Roth for Sandeep ($7.5k)")
    st.checkbox("March 11: Execute Backdoor Roth for Avanthi ($7.5k)")