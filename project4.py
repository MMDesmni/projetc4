#Importing libraries that we need

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

#Opening the pages

st.set_page_config(page_title="Crypto Charts", layout="wide")
st.title("Crypto Dashboard (Personal Edition)")

#Crypto currencies that we wanna show

ticker_list = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "BNB": "BNB-USD",
    "Cardano": "ADA-USD",
    "Solana": "SOL-USD",
    "Ripple": "XRP-USD"
}

#Selecting coins and how much we want

coins = st.multiselect("Pick your coins:", list(ticker_list.keys()), ["Bitcoin"])
days_back = st.slider("Days of history:", 30, 365, 120)

#Function for calculating sma20 sma50 ema20 and ema50

def indicators(df):
    df["sma20"] = df["Close"].rolling(20).mean()
    df["sma50"] = df["Close"].rolling(50).mean()
    df["ema20"] = df["Close"].ewm(span=20, adjust=False).mean()
    df["ema50"] = df["Close"].ewm(span=50, adjust=False).mean()

    return df

#For loop for showing coins

for coin in coins:
    st.subheader(f" {coin}")
    symbol = ticker_list[coin]
    
#For downloading data

    data = yf.download(symbol, period=f"{days_back}d")
    if data.empty:
        st.warning(f"No data found for {coin}")
        continue
    data = indicators(data)

#Plotting for showing chart

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data.Open,
        high=data.High,
        low=data.Low,
        close=data.Close,
        name="candles"
    ))
#Plotting for MACD and RSI indicators


    fig.add_trace(go.Scatter(x=data.index, y=data.sma20, line=dict(color="blue", width=1), name="SMA20"))
    fig.add_trace(go.Scatter(x=data.index, y=data.sma50, line=dict(color="orange", width=1), name="SMA50"))
    fig.add_trace(go.Scatter(x=data.index, y=data.ema20, line=dict(color="purple", width=1), name="EMA20"))
    fig.add_trace(go.Scatter(x=data.index, y=data.ema50, line=dict(color="green", width=1), name="EMA50"))

    fig.update_layout(
        title=f"{coin} price candles",
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

#Showing some basic information about the selected crypto currency

    st.write("Recent data:")
    st.dataframe(data.tail(5))