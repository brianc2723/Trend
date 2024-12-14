import streamlit as st
from pytrends.request import TrendReq
import time

st.title('Keyword Tracker')
keyword = st.text_input("Enter a keyword to track:")

if keyword:
    # Initialize TrendReq with a user-agent header
    pytrend = TrendReq(request_args={'headers': {'User-Agent': 'Mozilla/5.0'}})

    # Build payload for the keyword
    pytrend.build_payload(kw_list=[keyword])
    
    # Retry logic
    retries = 5
    for attempt in range(retries):
        try:
            # Fetch interest over time
            data = pytrend.interest_over_time()
            if not data.empty:
                st.write('You are tracking:', keyword)
                st.line_chart(data[keyword])
            else:
                st.write("No data found for this keyword.")
            break  # Exit loop if successful
        except Exception as e:
            if attempt < retries - 1:  # If not the last attempt
                st.warning(f"Attempt {attempt + 1} failed. Retrying...")
                time.sleep(5)  # Wait before retrying
            else:
                st.error("Failed to fetch data after several attempts. Please try again later.")
else:
    st.write("Please enter a keyword to track.")
