import streamlit as st
import pandas_datareader as pdr
import pandas as pd
import datetime as dt


def get_last_business_day():
    """
    Get last business day's date
    """
    today = dt.date.today()
    if today.weekday() == 5:  # Saturday
        last_business_day = today - dt.timedelta(days=1)
    elif today.weekday() == 6:  # Sunday
        last_business_day = today - dt.timedelta(days=2)
    else:
        last_business_day = today - dt.timedelta(days=1)
    return last_business_day


st.title('Stock Comparison App')

# Choose stocks to compare
tickers = st.multiselect('Choose stocks to compare', ['AAPL', 'GOOG', 'MSFT', 'AMZN'])

# Choose time frequency
freq_dict = {'Daily': 'D', 'Weekly': 'W', 'Monthly': 'M'}
freq = st.selectbox('Choose time frequency', list(freq_dict.keys()))

# Get start and end dates
end_date = get_last_business_day()
start_date = end_date - dt.timedelta(days=365)

# Get data for selected stocks
data = pdr.get_data_yahoo(tickers, start_date, end_date)

# Select 'Adj Close' prices for each stock
close_prices = data['Adj Close']

# Resample to selected frequency
close_prices = close_prices.resample(freq_dict[freq]).mean()

# Calculate returns
returns = close_prices.pct_change()

# Create a line chart for each stock
for ticker in tickers:
    st.line_chart(returns[ticker])
