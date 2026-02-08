import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Venture Scout V2", layout="wide")
st.title("⛏️ TSX Venture LifeCycle Scout")

# HELP TIP
st.sidebar.info("💡 Tip: Use .V for Venture (e.g., FUU.V) and .TO for TSX (e.g., LUN.TO)")
ticker_input = st.sidebar.text_input("Enter Ticker:", "FUU.V").upper()

if st.sidebar.button("Run Intelligence Screen"):
    with st.spinner('Accessing Exchange Data...'):
        stock = yf.Ticker(ticker_input)
        
        # We pull the last 3 years to see the full Lassonde Curve
        hist = stock.history(period="3y")

        if hist.empty:
            st.error(f"❌ Could not find {ticker_input}. Did you forget the .V suffix?")
        else:
            # 1. METRICS
            info = stock.info
            name = info.get('longName', ticker_input)
            price = hist['Close'].iloc[-1]
            peak = hist['Close'].max()
            drawdown = ((price - peak) / peak) * 100

            st.header(f"{name}")
            
            c1, c2, c3 = st.columns(3)
            # We use hist data if info['currentPrice'] returns N/A
            c1.metric("Current Price", f"${price:.3f}")
            c2.metric("3-Year High", f"${peak:.3f}")
            c3.metric("Drawdown", f"{drawdown:.1f}%")

            # 2. LASSONDE LOGIC
            st.subheader("📊 LifeCycle Phase")
            if drawdown < -60:
                st.success("🟢 PHASE: Potential Orphan Period (Accumulation Zone)")
            elif price > (hist['Close'].mean() * 1.5):
                st.warning("🔴 PHASE: Discovery Peak (High Speculation)")
            else:
                st.info("🔵 PHASE: Development / Working toward Production")

            # 3. CHART
            st.line_chart(hist['Close'])
