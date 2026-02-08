import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Venture Miner V2", layout="wide")
st.title("⛏️ Venture Mining Screener V2")

# Sidebar for Ticker Input
ticker = st.sidebar.text_input("Enter TSX.V Ticker:", value="FUU.V").upper()

if st.sidebar.button("Run Screener"):
    try:
        # Pull Live Data
        data = yf.Ticker(ticker)
        info = data.info
        
        # Display Metrics
        st.header(f"Results for {ticker}")
        c1, c2, c3 = st.columns(3)
        
        shares = info.get('sharesOutstanding', 0)
        cash = info.get('totalCash', 0)
        
        c1.metric("Shares Outstanding", f"{shares/1e6:.1f}M" if shares else "N/A")
        c2.metric("Cash (Est)", f"${cash/1e6:.1f}M" if cash else "N/A")
        c3.metric("Current Price", f"${info.get('currentPrice', 'N/A')}")
        
        # Screener Logic
        st.subheader("📋 Screener Checklist")
        if shares and shares < 100000000:
            st.success("✅ Tight Cap Structure (<100M shares)")
        else:
            st.warning("⚠️ High Share Count (>100M shares)")
            
        # Price Chart
        st.line_chart(data.history(period="1y")['Close'])
        
    except Exception as e:
        st.error(f"Could not find {ticker}. Did you forget the '.V'?")
