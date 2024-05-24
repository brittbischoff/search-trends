import streamlit as st

st.title('Search Trends Dashboard')
st.write('This is a simple Streamlit app to show search trends.')

# Example of an interactive widget
topic = st.text_input('Enter a topic:')
if topic:
    st.write(f'Search trends for {topic}')
    # Add your code to fetch and display search trends here

