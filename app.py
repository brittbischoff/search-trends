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

# Function to display rising queries
def display_rising_queries(rising_queries, timeframe):
    if rising_queries is not None and not rising_queries.empty:
        rising_queries.reset_index(inplace=True)
        st.subheader(f"Rising Queries - Last 7 Days ({timeframe})")
        st.write("Queries with the biggest increase in search frequency since the last time period. Results marked 'Breakout' had a tremendous increase, probably because these queries are new and had few (if any) prior searches.")
        for index, row in rising_queries.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(row['query'])
            with col2:
                if row['value'] == 'Breakout':
                    st.write('Breakout')
                else:
                    st.write(f"{row['value']}% increase")

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
                st.write(f"Top queries and rising queries for '{term}':")
                top_queries = us_related_queries[term]['top']
                rising_queries = us_related_queries[term]['rising']
                if top_queries is not None and not top_queries.empty:
                    wordcloud = create_wordcloud(top_queries)
                    if wordcloud:
                        fig, ax = plt.subplots(figsize=(8, 4))
                        ax.imshow(wordcloud, interpolation='bilinear')
                        ax.axis('off')
                        st.pyplot(fig)
                    else:
                        st.write(f"No wordcloud generated for '{term}'")
                if rising_queries is not None and not rising_queries.empty:
                    display_rising_queries(rising_queries.head(25), 'last 7 days')
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
                st.write(f"Top queries and rising queries for '{term}' in Arizona:")
                top_queries = arizona_related_queries[term]['top']
                rising_queries = arizona_related_queries[term]['rising']
                if top_queries is not None and not top_queries.empty:
                    wordcloud = create_wordcloud(top_queries)
                    if wordcloud:
                        fig, ax = plt.subplots(figsize=(8, 4))
                        ax.imshow(wordcloud, interpolation='bilinear')
                        ax.axis('off')
                        st.pyplot(fig)
                    else:
                        st.write(f"No wordcloud generated for '{term}' in Arizona")
                if rising_queries is not None and not rising_queries.empty:
                    display_rising_queries(rising_queries.head(25), 'last 7 days')
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
                st.write(f"Top queries and rising queries for '{term}' in Florida:")
                top_queries = florida_related_queries[term]['top']
                rising_queries = florida_related_queries[term]['rising']
                if top_queries is not None and not top_queries.empty:
                    wordcloud = create_wordcloud(top_queries)
                    if wordcloud:
                        fig, ax = plt.subplots(figsize=(8, 4))
                        ax.imshow(wordcloud, interpolation='bilinear')
                        ax.axis('off')
                        st.pyplot(fig)
                    else:
                        st.write(f"No wordcloud generated for '{term}' in Florida")
                if rising_queries is not None and not rising_queries.empty:
                    display_rising_queries(rising_queries.head(25), 'last 7 days')
    else:
        st.write('No data available for these search terms in Florida.')
