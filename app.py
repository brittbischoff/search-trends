import streamlit as st
from pytrends.request import TrendReq
import pandas as pd

# Function to fetch Google Trends data for multiple search terms
def get_trends_data(search_terms, geo=''):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(search_terms, cat=0, timeframe='today 12-m', geo=geo, gprop='')
    data = pytrends.interest_over_time()
    if not data.empty:
        data = data.drop(labels=['isPartial'], axis='columns')
    return data

# Streamlit app
st.title('Google Search Trends')

# Input widget for multiple search terms
search_terms = st.text_input('Enter search terms or topics (comma-separated):')

# Display global search trends data
if search_terms:
    search_terms_list = [term.strip() for term in search_terms.split(',')]
    st.write(f'Global search trends for: {", ".join(search_terms_list)}')
    global_data = get_trends_data(search_terms_list)
    if not global_data.empty:
        st.line_chart(global_data)
    else:
        st.write('No global data available for these search terms.')

    st.write(f'Search trends for: {", ".join(search_terms_list)} in Arizona')
    arizona_data = get_trends_data(search_terms_list, geo='US-AZ')
    if not arizona_data.empty:
        st.line_chart(arizona_data)
    else:
        st.write('No data available for these search terms in Arizona.')

    st.write(f'Search trends for: {", ".join(search_terms_list)} in Florida')
    florida_data = get_trends_data(search_terms_list, geo='US-FL')
    if not florida_data.empty:
        st.line_chart(florida_data)
    else:
        st.write('No data available for these search terms in Florida.')
