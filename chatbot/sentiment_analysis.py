from textblob import TextBlob
import matplotlib.pyplot as plt
import streamlit as st
from chatbot.chat_history import load_chat_sessions

def get_sentiment_label(polarity):
    if polarity < -0.6:
        return "Very Negative"
    elif polarity < -0.2:
        return "Negative"
    elif polarity < 0.2:
        return "Neutral"
    elif polarity < 0.6:
        return "Positive"
    else:
        return "Very Positive"

def analyze_session_sentiment(sessions):
    session_sentiments = []
    session_names = []
    for session in sessions:
        sentiments = [TextBlob(message['parts']).sentiment.polarity for message in session['messages'] if message['role'] == 'user']
        if sentiments:
            avg_sentiment = sum(sentiments) / len(sentiments)
            sentiment_label = get_sentiment_label(avg_sentiment)
            session_sentiments.append(sentiment_label)
            session_names.append(session['session_id']) 
    return session_sentiments, session_names

def plot_session_sentiments(session_sentiments, session_names):
    plt.figure(figsize=(10, 5))
    plt.plot(session_names, session_sentiments, marker='o')
    plt.title('Sentiment Analysis Across Sessions')
    plt.xlabel('Session')
    plt.ylabel('Sentiment')
    plt.xticks(rotation=45, ha="right")
    plt.grid(True)
    st.pyplot(plt)

    st.write("### Sentiment Analysis Explanation")
    st.write("""
        This graph shows the sentiment trend across different chat sessions. 
        The y-axis represents the average sentiment of each session, categorized into labels such as 'Very Negative', 'Negative', 'Neutral', 'Positive', and 'Very Positive'. 
        The x-axis represents the different sessions identified by their unique IDs. 
        This visualization helps in understanding the emotional tone of the user's interactions over time.
    """)

def display_sentiment_analysis(db, username):
    sessions = load_chat_sessions(db, username)
    if sessions:
        session_sentiments, session_names = analyze_session_sentiment(sessions)
        if session_sentiments:
            plot_session_sentiments(session_sentiments, session_names)
        else:
            st.write("No sentiment data available for analysis.")
    else:
        st.write("No chat sessions available for analysis.")
