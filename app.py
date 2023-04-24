import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title('Stock Comparison App')

# User input
ticker1 = st.text_input('Enter the first ticker:')
ticker2 = st.text_input('Enter the second ticker:')
time_frame = st.selectbox('Select the time frame:', ('日K线', '月K线', '年K线'))

# Retrieve data from Yahoo finance
start_date = '2010-01-01'
end_date = '2023-4-23'

data1 = yf.download(ticker1, start=start_date, end=end_date)
data2 = yf.download(ticker2, start=start_date, end=end_date)

df1 = pd.DataFrame(data1['Adj Close'])
df2 = pd.DataFrame(data2['Adj Close'])

# Resample data based on selected time frame
if time_frame == '日K线':
    df1.index = pd.to_datetime(df1.index)
    df2.index = pd.to_datetime(df2.index)
elif time_frame == '月K线':
    df1.index = pd.to_datetime(df1.index).to_period('M')
    df2.index = pd.to_datetime(df2.index).to_period('M')
else:
    df1.index = pd.to_datetime(df1.index).to_period('Y')
    df2.index = pd.to_datetime(df2.index).to_period('Y')

df1 = df1.mean(level=0)
df2 = df2.mean(level=0)

# Compare stock price trends
st.write('### Stock Price Comparison')
fig, ax = plt.subplots()
ax.plot(df1.index, df1.values, label=ticker1)
ax.plot(df2.index, df2.values, label=ticker2)
ax.set_xlabel('Year')
ax.set_ylabel('Adjusted Close Price ($)')
ax.legend()
st.pyplot(fig)

# Calculate and compare stock returns
returns1 = df1.pct_change()
returns2 = df2.pct_change()

st.write('### Stock Return Comparison')
fig, ax = plt.subplots()
ax.plot(returns1.index, returns1.values, label=ticker1)
ax.plot(returns2.index, returns2.values, label=ticker2)
ax.set_xlabel('Year')
ax.set_ylabel('Return')
ax.legend()
st.pyplot(fig)
