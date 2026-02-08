import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Venture Miner V2", layout="wide")
st.title("⛏️ Venture Mining Scout V2")

ticker = st.sidebar.text_input("Enter Ticker (e.g. FUU.V):", value="FUU.V").upper()

if st.sidebar.button("Run Screener"):
    # Clear previous errors
    st.empty()
    
    with st.spinner(f'Fetching live data for {ticker}...'):
        data = yf.Ticker(ticker)
        
        # 1. Try to get Price History first (most reliable)
        hist = data.history(period="1y")
        
        if hist.empty:
            st.error(f"❌ No data found for {ticker}. Check the ticker suffix (use .V for Venture).")
        else:
            # 2. Get Info (Fragile)
            info = data.info
            
            # Display Metrics with "Fallback" values
            c1, c2, c3 = st.columns(3)
            
            price = info.get('currentPrice') or (hist['Close'].iloc[-1] if not hist.empty else 0)
            shares = info.get('sharesOutstanding', 0)
            cash = info.get('totalCash', 0)
            
            c1.metric("Shares Outstanding", f"{shares/1e6:.1f}M" if shares else "Data Pending")
            c2.metric("Cash (Est)", f"${cash/1e6:.1f}M" if cash else "Data Pending")
            c3.metric("Current Price", f"${price:.3f}")
            
            # 3. Apply Screener
            st.subheader("📋 Quick-Score Analysis")
            if shares and shares < 100000000:
                st.success("✅ Tight Cap Structure")
            else:
                st.info("ℹ️ Share structure data currently unavailable or count high.")
                
            st.line_chart(hist['Close'])
