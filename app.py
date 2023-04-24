import streamlit as st
import pandas as pd
import yfinance as yf
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class StockWatcher(FileSystemEventHandler):
    def __init__(self):
        self.df1 = None
        self.df2 = None

    def on_modified(self, event):
        self.load_data()

    def load_data(self):
        try:
            ticker1 = 'BRK-B'
            ticker2 = 'TSLA'
            df1 = yf.download(ticker1, period='max')
            df2 = yf.download(ticker2, period='max')
            if not df1.empty and not df2.empty:
                self.df1 = df1['Close']
                self.df2 = df2['Close']
        except:
            pass


def main():
    # Watch file changes
    observer = Observer()
    event_handler = StockWatcher()
    observer.schedule(event_handler, '.', recursive=False)
    observer.start()

    # Load initial data
    event_handler.load_data()

    # Streamlit app
    st.title('Stock Comparison')

    if event_handler.df1 is None or event_handler.df2 is None:
        st.write('Loading data...')
        return

    # Choose time frame
    time_frame = st.selectbox('Time Frame', ['日K线', '月K线', '年K线'])

    # Resample data according to time frame
    if time_frame == '日K线':
        df1 = event_handler.df1.resample('D').mean().dropna()
        df2 = event_handler.df2.resample('D').mean().dropna()
    elif time_frame == '月K线':
        df1 = event_handler.df1.resample('M').mean().dropna()
        df2 = event_handler.df2.resample('M').mean().dropna()
    else:
        df1 = event_handler.df1.resample('Y').mean().dropna()
        df2 = event_handler.df2.resample('Y').mean().dropna()

    # Compare stock prices
    comparison = df1.to_frame(name='BRK-B').join(df2.to_frame(name='TSLA')).dropna()
    comparison['BRK-B/TSLA'] = comparison['BRK.B'] / comparison['TSLA']

    # Show comparison chart
    st.line_chart(comparison[['BRK-B', 'TSLA']])
    st.line_chart(comparison['BRK-B/TSLA'])


if __name__ == '__main__':
    main()

