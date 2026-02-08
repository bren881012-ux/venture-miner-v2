import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Lassonde Scout", layout="wide")
st.title("⛏️ Lassonde Lifecycle Visualizer")

# 1. INPUT
ticker = st.sidebar.text_input("Enter TSX.V Ticker (e.g., FUU.V):", "FUU.V").upper()

if st.sidebar.button("Analyze LifeCycle"):
    data = yf.Ticker(ticker)
    hist = data.history(period="3y") # 3 years captures the full curve phases

    if hist.empty:
        st.error("No data found. Did you add '.V'?")
    else:
        # 2. CALCULATE PHASES (The 'Brain' Logic)
        peak = hist['Close'].max()
        current = hist['Close'].iloc[-1]
        drawdown = ((current - peak) / peak) * 100
        
        # Identify Phase
        if drawdown < -50:
            phase = "Orphan Period (Value Zone)"
            color = "#00FF00" # Green
        elif current > (hist['Close'].mean() * 1.8):
            phase = "Discovery Peak (Hype Zone)"
            color = "#FF0000" # Red
        else:
            phase = "Development Phase"
            color = "#0000FF" # Blue

        # 3. DISPLAY HEADER
        st.subheader(f"Current Status: :{color}[{phase}]")
        st.metric("Drawdown from Peak", f"{drawdown:.1f}%")

        # 4. THE INTERACTIVE CHART
        fig = go.Figure()

        # The Price Line
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name="Share Price", line=dict(color='white', width=2)))

        # Add "Discovery Peak" Marker
        peak_date = hist['Close'].idxmax()
        fig.add_annotation(x=peak_date, y=peak, text="Discovery Peak", showarrow=True, arrowhead=1, bgcolor="red")

        # Layout styling for 'Dark Mode' mining feel
        fig.update_layout(template="plotly_dark", title=f"{ticker} LifeCycle Chart", xaxis_title="Timeline", yaxis_title="Price (CAD)")
        
        st.plotly_chart(fig, use_container_width=True)

        st.info("💡 **Tip:** Look for 'U-Shaped' bottoms after a 50%+ drawdown. This often signals the transition from Orphan to Development.")
