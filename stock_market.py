import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go

# Set the title of the dashboard
st.title('Stock Market Dashboard')

# Sidebar for user input
st.sidebar.header('User Input')

# User input for stock ticker
ticker = st.sidebar.text_input('Enter Stock Ticker', 'AAPL')
period = st.sidebar.selectbox('Select Period', ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max'])

# Fetching stock data
def get_stock_data(ticker, period='1y'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data

# Fetch data for the primary ticker
data = get_stock_data(ticker, period)

# Display the stock data in a table
st.subheader(f'{ticker} Stock Data')
st.write(data)

# Plotting stock prices using Matplotlib
st.subheader(f"{ticker} Price Chart")
plt.figure(figsize=(10, 5))
plt.plot(data['Close'], label='Close Price')
plt.title(f"{ticker} Price Over Time")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
st.pyplot(plt)

# Calculating and plotting moving averages
data['50_MA'] = data['Close'].rolling(window=50).mean()
data['200_MA'] = data['Close'].rolling(window=200).mean()

plt.figure(figsize=(10, 5))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['50_MA'], label='50-Day MA', linestyle='--')
plt.plot(data['200_MA'], label='200-Day MA', linestyle='--')
plt.title(f"{ticker} Price with Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
st.pyplot(plt)

# Comparative Analysis
st.sidebar.header('Comparative Analysis')
compare_tickers = st.sidebar.text_input('Compare Tickers (comma separated)', 'AAPL, MSFT, GOOG')

if compare_tickers:
    tickers_list = compare_tickers.split(',')
    fig_comp = go.Figure()

    for comp_ticker in tickers_list:
        comp_data = get_stock_data(comp_ticker.strip(), period)
        fig_comp.add_trace(go.Scatter(x=comp_data.index, y=comp_data['Close'], mode='lines', name=comp_ticker.strip()))

    fig_comp.update_layout(title='Comparative Stock Prices',
                            xaxis_title='Date',
                            yaxis_title='Price (USD)',
                            legend_title='Stock Tickers')
    st.plotly_chart(fig_comp)

# Downloadable report
st.sidebar.subheader("Download Data")
if st.sidebar.button("Download CSV"):
    data.to_csv(f"{ticker}_data.csv")
    st.sidebar.success("Download successful!")
