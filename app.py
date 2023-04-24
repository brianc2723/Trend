import yfinance as yf
import streamlit as st
import pandas as pd

# Set page title
st.set_page_config(page_title="Stock Comparison App")

# Define function to get stock data
@st.cache
def get_data(tickers, start_date, end_date):
    """
    This function gets stock data from Yahoo Finance API
    """
    data = yf.download(tickers=tickers, start=start_date, end=end_date)
    return data

# Define function to plot stock data
def plot_data(df1, df2):
    """
    This function plots the stock data
    """
    # Calculate returns
    df1['Returns'] = df1['Close'].pct_change()
    df2['Returns'] = df2['Close'].pct_change()

    # Calculate cumulative returns
    df1['Cumulative Returns'] = (1 + df1['Returns']).cumprod()
    df2['Cumulative Returns'] = (1 + df2['Returns']).cumprod()

    # Plot cumulative returns
    fig1 = df1['Cumulative Returns'].plot(title=ticker1 + ' Cumulative Returns', label=ticker1)
    df2['Cumulative Returns'].plot(title=ticker2 + ' Cumulative Returns', label=ticker2)
    fig1.set_xlabel("Date")
    fig1.set_ylabel("Cumulative Returns")

    # Plot daily returns
    fig2 = df1['Returns'].plot(title=ticker1 + ' Daily Returns', label=ticker1)
    df2['Returns'].plot(title=ticker2 + ' Daily Returns', label=ticker2)
    fig2.set_xlabel("Date")
    fig2.set_ylabel("Daily Returns")

# Set page title
st.title("Stock Comparison App")

# Define sidebar inputs
st.sidebar.title("Inputs")
ticker1 = st.sidebar.text_input("Enter first ticker (e.g. BRK.B)", value="BRK.B")
ticker2 = st.sidebar.text_input("Enter second ticker (e.g. TSLA)", value="TSLA")
start_date = st.sidebar.date_input("Start date", value=pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End date", value=pd.to_datetime("today"))
time_frame = st.sidebar.selectbox("Select time frame", ["日K线", "月K线", "年K线"])

# Get stock data
data = get_data([ticker1, ticker2], start_date, end_date)

# Select data based on time frame
if time_frame == '日K线':
    data = data.resample('D').mean().dropna()
elif time_frame == '月K线':
    data = data.resample('M').mean().dropna()
else:
    data = data.resample('Y').mean().dropna()

# Split data for each ticker
df1 = pd.DataFrame(data[ticker1])
df2 = pd.DataFrame(data[ticker2])

# Plot data
plot_data(df1, df2)
st.pyplot()
