import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_option('deprecation.showPyplotGlobalUse', False)

st.write("""
# 股票升跌幅度比较
""")

# 股票代码输入
expander = st.beta_expander("输入股票代码")
with expander:
    option = st.selectbox('选择数据源', ('yahoo', 'google'))
    stock1 = st.text_input("输入第一只股票代码", 'BRK-B')
    stock2 = st.text_input("输入第二只股票代码", 'TSLA')

# 时间周期选择
time_frame = st.sidebar.selectbox('选择时间周期', ('日K线', '月K线', '年K线'))

# 获取数据
data = yf.download([stock1, stock2], period='max', interval='1d', group_by='ticker', auto_adjust=True, prepost=True, threads=True, proxy=None)

# 获取两只股票的涨跌幅
df1 = pd.DataFrame(data[stock1]['Close'].pct_change())
df2 = pd.DataFrame(data[stock2]['Close'].pct_change())

# 根据时间周期重采样数据
if time_frame == '日K线':
    df1 = df1.resample('D').mean().dropna()
    df2 = df2.resample('D').mean().dropna()
elif time_frame == '月K线':
    df1 = df1.resample('M').mean().dropna()
    df2 = df2.resample('M').mean().dropna()
else:
    df1 = df1.resample('Y').mean().dropna()
    df2 = df2.resample('Y').mean().dropna()

# 绘制折线图
fig, ax = plt.subplots()
sns.lineplot(data=df1, ax=ax, label=stock1)
sns.lineplot(data=df2, ax=ax, label=stock2)
ax.set(xlabel='日期', ylabel='涨跌幅', title=f'{stock1}与{stock2}涨跌幅比较 ({time_frame})')
st.pyplot(fig)

# 绘制条形图
diff = (df1 - df2).dropna()
fig, ax = plt.subplots()
sns.barplot(data=diff, ax=ax)
ax.set(xlabel='日期', ylabel='涨跌幅差', title=f'{stock1}与{stock2}涨跌幅差比较 ({time_frame})')
st.pyplot(fig)

