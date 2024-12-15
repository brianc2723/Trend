import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import requests

# Initialize Pytrends
pytrend = TrendReq()

# Function to fetch Google Trends data
def fetch_trends(keyword):
    pytrend.build_payload(kw_list=[keyword])
    data = pytrend.interest_over_time()
    return data

# Function to fetch news articles from Google News API
def fetch_news(query):
    api_key = 'YOUR_NEWS_API_KEY'  # Replace with your actual News API key
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={api_key}'
    response = requests.get(url)
    return response.json()

# Streamlit UI setup
st.title('Keyword Tracker with AI Chatbot and News')

# Keyword input for Google Trends
keyword = st.text_input("Enter a keyword to track:")

if keyword:
    trends_data = fetch_trends(keyword)
    if not trends_data.empty:
        st.line_chart(trends_data[keyword])
    else:
        st.write("No data found for this keyword.")

    # Fetch and display news articles related to the keyword
    news_data = fetch_news(keyword)
    if news_data['status'] == 'ok':
        articles = news_data['articles']
        for article in articles[:5]:  # Display top 5 articles
            st.subheader(article['title'])
            st.write(article['description'])
            st.write(f"[Read more]({article['url']})")
    else:
        st.write("Failed to fetch news articles.")

# Ollama Chatbot Integration (Basic Example)
st.subheader('Chat with our AI')
user_input = st.text_input("Ask something:")
if user_input:
    # Here you would call your Ollama model API or function to get a response.
    # For example:
    # response = ollama_chatbot.get_response(user_input)
    
    # Placeholder response for demonstration purposes.
    response = "This is where the AI's response will appear."
    
    st.write(f"AI: {response}")

