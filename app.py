import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Stock Comparison App")

st.title("Stock Comparison App")

# 輸入股票代號
ticker_list = []
while True:
    ticker = st.text_input("請輸入股票代號（例如 AAPL）：")
    if ticker:
        ticker_list.append(ticker.upper())
    else:
        break

# 選擇時間區間
time_interval = st.selectbox("請選擇時間區間：", ["1日K", "1月K", "1年K"])

# 取得收盤價數據
df = pd.DataFrame()
for ticker in ticker_list:
    stock_data = yf.Ticker(ticker).history(period=time_interval.lower())
    stock_data = stock_data[['Close']]
    stock_data = stock_data.rename(columns={'Close': ticker})
    df = pd.concat([df, stock_data], axis=1)

# 計算每支股票的漲跌幅
price_diff = df.pct_change().dropna()

# 計算每支股票的總漲跌幅
total_diff = price_diff.sum()

# 計算每支股票的相對漲跌幅
relative_diff = total_diff / len(ticker_list)

# 顯示比較結果
st.subheader("比較結果：")
st.write(price_diff)
st.write("每支股票的總漲跌幅：", total_diff)
st.write("每支股票的相對漲跌幅：", relative_diff)
