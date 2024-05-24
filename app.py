import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import time
from pytrends.exceptions import TooManyRequestsError

# Function to fetch Google Trends data and related queries with rate limiting
def get_trends_data(search_terms, geo=''):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(search_terms, cat=0, timeframe='today 12-m', geo=geo, gprop='')
    
    # Retry logic for handling TooManyRequestsError
    attempts = 0
    while attempts < 5:
        try:
            data = pytrends.interest_over_time()
            related_queries = pytrends.related_queries()
            if not data.empty:
                data = data.drop(labels=['isPartial'], axis='columns')
            return data, related_queries
        except TooManyRequestsError:
            attempts += 1
            st.warning("Rate limit reached, retrying...")
            time.sleep(60)  # Wait for 60 seconds before retrying
    st.error("Failed to fetch data after several attempts due to rate limiting.")
    return pd.DataFrame(), {}

# Streamlit app
st.title('Google Search Trends')

# Input widget for multiple search terms
search_terms = st.text_input('Enter search terms or topics (comma-separated):')

# Display global search trends data
if search_terms:
    search_terms_list = [term.strip() for term in search_terms.split(',')]
    st.write(f'Global search trends for: {", ".join(search_terms_list)}')
    global_data, global_related_queries = get_trends_data(search_terms_list)
    if not global_data.empty:
        st.line_chart(global_data)
        st.write("Global related queries and top queries:")
        for term in search_terms_list:
            if term in global_related_queries:
                st.write(f"Related queries for '{term}':")
                st.write(global_related_queries[term]['top'])
                st.write(f"Rising queries for '{term}':")
                st.write(global_related_queries[term]['rising'])
    else:
        st.write('No global data available for these search terms.')

    st.write(f'Search trends for: {", ".join(search_terms_list)} in Arizona')
    arizona_data, arizona_related_queries = get_trends_data(search_terms_list, geo='US-AZ')
    if not arizona_data.empty:
        st.line_chart(arizona_data)
        st.write("Arizona related queries and top queries:")
        for term in search_terms_list:
            if term in arizona_related_queries:
                st.write(f"Related queries for '{term}':")
                st.write(arizona_related_queries[term]['top'])
                st.write(f"Rising queries for '{term}':")
                st.write(arizona_related_queries[term]['rising'])
    else:
        st.write('No data available for these search terms in Arizona.')

    st.write(f'Search trends for: {", ".join(search_terms_list)} in Florida')
    florida_data, florida_related_queries = get_trends_data(search_terms_list, geo='US-FL')
    if not florida_data.empty:
        st.line_chart(florida_data)
        st.write("Florida related queries and top queries:")
        for term in search_terms_list:
            if term in florida_related_queries:
                st.write(f"Related queries for '{term}':")
                st.write(florida_related_queries[term]['top'])
                st.write(f"Rising queries for '{term}':")
                st.write(florida_related_queries[term]['rising'])
    else:
        st.write('No data available for these search terms in Florida.')
