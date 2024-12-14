import streamlit as st
from pytrends.request import TrendReq

st.title('Keyword Tracker')
keyword = st.text_input("Enter a keyword to track:")

if keyword:
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=[keyword])
    
    # Fetch interest over time
    data = pytrend.interest_over_time()

    # Check if data is available
    if not data.empty:
        st.write('You are tracking:', keyword)
        st.line_chart(data[keyword])
    else:
        st.write("No data found for this keyword.")
else:
    st.write("Please enter a keyword to track.")
