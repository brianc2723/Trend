import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 设置页面标题
st.title('Stock Comparison App')

# 添加用户输入
col1, col2 = st.beta_columns(2)
with col1:
    stock1 = st.text_input('请输入第一支股票代码（例如AAPL）：')
with col2:
    stock2 = st.text_input('请输入第二支股票代码（例如AMZN）：')

# 添加用户选择
time_frame = st.radio("请选择时间周期：", ("日K线", "月K线", "年K线"))

# 获取数据并绘图
@st.cache
def get_data(stock1, stock2):
    ticker1 = yf.Ticker(stock1)
    ticker2 = yf.Ticker(stock2)
    df1 = ticker1.history(period="max")
    df2 = ticker2.history(period="max")
    return df1, df2

df1, df2 = get_data(stock1, stock2)

if time_frame == '日K线':
    df1 = df1.resample('D').mean().dropna()
    df2 = df2.resample('D').mean().dropna()
elif time_frame == '月K线':
    df1 = df1.resample('M').mean().dropna()
    df2 = df2.resample('M').mean().dropna()
else:
    df1 = df1.resample('Y').mean().dropna()
    df2 = df2.resample('Y').mean().dropna()

if len(df1) == 0 or len(df2) == 0:
    st.write("输入的股票代码有误，请重新输入！")
else:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df1.index, df1['Close']/df1['Close'][0], label=stock1)
    ax.plot(df2.index, df2['Close']/df2['Close'][0], label=stock2)
    ax.set_xlabel('时间')
    ax.set_ylabel('股票价格相对初始值的比例')
    ax.legend(loc='best')
    st.pyplot(fig)

