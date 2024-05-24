import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
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

# Function to create a word cloud from query data
def create_wordcloud(query_data):
    if query_data is not None and not query_data.empty:
        query_text = ' '.join(query_data['query'].tolist())
        wordcloud = WordCloud(width=800, height=400, max_words=25, background_color='white').generate(query_text)
        return wordcloud
    return None

# Streamlit app
st.title('Google Search Trends')

# Fixed search terms and topics
fixed_terms = ['Python programming', 'Data Science']
fixed_topics = ['Machine Learning', 'Artificial Intelligence']

# Input widget for additional search terms
additional_terms = st.text_input('Enter additional search terms or topics (comma-separated):')

# Combine fixed terms/topics with user input
if additional_terms:
    user_terms = [term.strip() for term in additional_terms.split(',')]
    search_terms_list = fixed_terms + fixed_topics + user_terms
else:
    search_terms_list = fixed_terms + fixed_topics

# Display global search trends data
st.write(f'Global search trends for: {", ".join(search_terms_list)}')
global_data, global_related_queries = get_trends_data(search_terms_list)
if not global_data.empty:
    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(global_data)
    with col2:
        st.write("Global related queries word cloud:")
        for term in search_terms_list:
            if term in global_related_queries:
                top_queries = global_related_queries[term]['top']
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
else:
    st.write('No global data available for these search terms.')

# Display search trends data for Arizona
st.write(f'Search trends for: {", ".join(search_terms_list)} in Arizona')
arizona_data, arizona_related_queries = get_trends_data(search_terms_list, geo='US-AZ')
if not arizona_data.empty:
    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(arizona_data)
    with col2:
        st.write("Arizona related queries word cloud:")
        for term in search_terms_list:
            if term in arizona_related_queries:
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
else:
    st.write('No data available for these search terms in Arizona.')

# Display search trends data for Florida
st.write(f'Search trends for: {", ".join(search_terms_list)} in Florida')
florida_data, florida_related_queries = get_trends_data(search_terms_list, geo='US-FL')
if not florida_data.empty:
    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(florida_data)
    with col2:
        st.write("Florida related queries word cloud:")
        for term in search_terms_list:
            if term in florida_related_queries:
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
else:
    st.write('No data available for these search terms in Florida.')
