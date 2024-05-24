import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time
from pytrends.exceptions import TooManyRequestsError

# Function to fetch Google Trends data and related queries with rate limiting
def get_trends_data(search_terms, geo='US', timeframe='today 12-m'):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(search_terms, cat=0, timeframe=timeframe, geo=geo, gprop='')
    
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

# Function to create a word cloud from query data
def create_wordcloud(query_data):
    if query_data is not None and not query_data.empty:
        query_text = ' '.join(query_data['query'].tolist())
        wordcloud = WordCloud(width=800, height=400, max_words=25, background_color='white').generate(query_text)
        return wordcloud
    return None

# Streamlit app
st.title('Google Search Trends')

# Input widget for search terms
search_terms = st.text_input('Enter search terms or topics (comma-separated):')

# Display search trends data
if search_terms:
    search_terms_list = [term.strip() for term in search_terms.split(',')]
    st.write(f'Search trends for: {", ".join(search_terms_list)} in the United States')
    
    # United States trends
    us_data, us_related_queries = get_trends_data(search_terms_list)
    if not us_data.empty:
        st.line_chart(us_data)
        st.write("United States related queries word cloud and rising queries:")
        for term in search_terms_list:
            if term in us_related_queries:
                col1, col2 = st.columns(2)
                with col1:
                    top_queries = us_related_queries[term]['top']
                    if top_queries is not None and not top_queries.empty:
                        st.write(f"Top queries for '{term}':")
                        wordcloud = create_wordcloud(top_queries)
                        if wordcloud:
                            fig, ax = plt.subplots(figsize=(8, 4))
                            ax.imshow(wordcloud, interpolation='bilinear')
                            ax.axis('off')
                            st.pyplot(fig)
                        else:
                            st.write(f"No wordcloud generated for '{term}'")
                with col2:
                    rising_queries = us_related_queries[term]['rising']
                    if rising_queries is not None and not rising_queries.empty:
                        st.write(f"Rising queries for '{term}' in the last 7 days:")
                        st.write(rising_queries.head(25))
    else:
        st.write('No data available for these search terms in the United States.')

    # Arizona trends
    st.write(f'Search trends for: {", ".join(search_terms_list)} in Arizona')
    arizona_data, arizona_related_queries = get_trends_data(search_terms_list, geo='US-AZ')
    if not arizona_data.empty:
        st.line_chart(arizona_data)
        st.write("Arizona related queries word cloud and rising queries:")
        for term in search_terms_list:
            if term in arizona_related_queries:
                col1, col2 = st.columns(2)
                with col1:
                    top_queries = arizona_related_queries[term]['top']
                    if top_queries is not None and not top_queries.empty:
                        st.write(f"Top queries for '{term}' in Arizona:")
                        wordcloud = create_wordcloud(top_queries)
                        if wordcloud:
                            fig, ax = plt.subplots(figsize=(8, 4))
                            ax.imshow(wordcloud, interpolation='bilinear')
                            ax.axis('off')
                            st.pyplot(fig)
                        else:
                            st.write(f"No wordcloud generated for '{term}' in Arizona")
                with col2:
                    rising_queries = arizona_related_queries[term]['rising']
                    if rising_queries is not None and not rising_queries.empty:
                        st.write(f"Rising queries for '{term}' in Arizona in the last 7 days:")
                        st.write(rising_queries.head(25))
    else:
        st.write('No data available for these search terms in Arizona.')

    # Florida trends
    st.write(f'Search trends for: {", ".join(search_terms_list)} in Florida')
    florida_data, florida_related_queries = get_trends_data(search_terms_list, geo='US-FL')
    if not florida_data.empty:
        st.line_chart(florida_data)
        st.write("Florida related queries word cloud and rising queries:")
        for term in search_terms_list:
            if term in florida_related_queries:
                col1, col2 = st.columns(2)
                with col1:
                    top_queries = florida_related_queries[term]['top']
                    if top_queries is not None and not top_queries.empty:
                        st.write(f"Top queries for '{term}' in Florida:")
                        wordcloud = create_wordcloud(top_queries)
                        if wordcloud:
                            fig, ax = plt.subplots(figsize=(8, 4))
                            ax.imshow(wordcloud, interpolation='bilinear')
                            ax.axis('off')
                            st.pyplot(fig)
                        else:
                            st.write(f"No wordcloud generated for '{term}' in Florida")
                with col2:
                    rising_queries = florida_related_queries[term]['rising']
                    if rising_queries is not None and not rising_queries.empty:
                        st.write(f"Rising queries for '{term}' in Florida in the last 7 days:")
                        st.write(rising_queries.head(25))
    else:
        st.write('No data available for these search terms in Florida.')
