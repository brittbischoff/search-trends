import streamlit as st
from pytrends.request import TrendReq
import pandas as pd

# Function to fetch Google Trends data
def get_trends_data(search_term):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([search_term], cat=0, timeframe='today 12-m', geo='', gprop='')
    data = pytrends.interest_over_time()
    if not data.empty:
        data = data.drop(labels=['isPartial'], axis='columns')
    return data

# Streamlit app
st.title('Google Search Trends')

# Input widget
search_term = st.text_input('Enter a search term or topic:')

# Display search trends data
if search_term:
    st.write(f'Search trends for "{search_term}"')
    data = get_trends_data(search_term)
    if not data.empty:
        st.line_chart(data)
    else:
        st.write('No data available for this search term.')
