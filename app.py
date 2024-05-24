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

# Input widget for multiple search terms
search_terms = st.text_input('Enter search terms or topics (comma-separated):')

# Display global search trends data
if search_terms:
    search_terms_list = [term.strip() for term in search_terms.split(',')]
    st.write(f'Global search trends for: {", ".join(search_terms_list)}')
    global_data, global_related_queries = get_trends_data(search_terms_list)
    if not global_data.empty:
        st.line_chart(global_data)
        st.write("Global related queries word cloud:")
        for term in search_terms_list:
            if term in global_related_queries:
                top_queries = global_related_queries[term]['top']
                wordcloud = create_wordcloud(top_queries)
                if wordcloud:
                    plt.figure(figsize=(10, 5))
                    plt.imshow(wordcloud, interpolation='bilinear')
          
