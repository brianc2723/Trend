import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, ".", recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            print(f"Received created event - {event.src_path}.")
            plot_data()


def plot_data():
    df1 = yf.download("BRK-B", period="max")
    df2 = yf.download("TSLA", period="max")
    
    df1 = df1.resample('D').last().ffill().pct_change().dropna()
    df2 = df2.resample('D').last().ffill().pct_change().dropna()

    sns.set(style="darkgrid", palette="bright", font_scale=1.5)
    plt.figure(figsize=(20,10))
    plt.plot(df1, label='BRK-B')
    plt.plot(df2, label='TSLA')
    plt.legend(loc='best')
    plt.title("Daily Returns Comparison")
    plt.xlabel('Date')
    plt.ylabel('Daily Returns')
    st.pyplot()

    df1 = df1.resample('M').mean().dropna()
    df2 = df2.resample('M').mean().dropna()
    sns.set(style="darkgrid", palette="bright", font_scale=1.5)
    plt.figure(figsize=(20,10))
    plt.plot(df1, label='BRK-B')
    plt.plot(df2, label='TSLA')
    plt.legend(loc='best')
    plt.title("Monthly Returns Comparison")
    plt.xlabel('Date')
    plt.ylabel('Monthly Returns')
    st.pyplot()

    df1 = df1.resample('Y').mean().dropna()
    df2 = df2.resample('Y').mean().dropna()
    sns.set(style="darkgrid", palette="bright", font_scale=1.5)
    plt.figure(figsize=(20,10))
    plt.plot(df1, label='BRK-B')
    plt.plot(df2, label='TSLA')
    plt.legend(loc='best')
    plt.title("Yearly Returns Comparison")
    plt.xlabel('Date')
    plt.ylabel('Yearly Returns')
    st.pyplot()

if __name__ == '__main__':
    st.set_page_config(page_title="Stock Comparison App")
    st.title("Stock Comparison App")
    st.write("This app compares the daily, monthly, and yearly returns of Berkshire Hathaway (BRK-B) and Tesla (TSL
