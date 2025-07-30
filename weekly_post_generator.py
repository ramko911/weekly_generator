import streamlit as st
from datetime import date, timedelta
import pandas as pd
import re
import os

st.set_page_config(
    page_title="Wantumeni Post Generator",
    page_icon="favicon.png",
    layout="centered"
)

st.title("🎧 Wantumeni Post Generator")

# File paths
HISTORY_FILE = "post_history.csv"
ANALYTICS_FILE = "analytics.csv"

# Helpers
def delete_row(df, index):
    return df.drop(index=index).reset_index(drop=True)

def generate_hashtags(title, artist, sample):
    base = ["#boombap", "#hiphopinstrumental", "#beatmaker"]
    artist_tag = f"#{re.sub(r'[^a-zA-Z0-9]', '', artist.replace(' ', '').lower())}" if artist else ""
    sample_tag = f"#{re.sub(r'\\s+', '', sample.lower())}" if sample else ""
    extra = ["#sampling", "#vinyl", "#soulful", "#typebeat"]
    return base + [artist_tag, sample_tag] + extra

# Tabs
tab0, tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📄 Description", "📜 History", "📊 Analytics", "🪄 AI Descriptions"])

with tab0:
    st.header("Weekly Digest")
    st.write("Top performer, engagement, trends, and insights coming soon.")

with tab1:
    st.header("Post Description Generator")
    st.write("Form goes here to generate platform descriptions.")

with tab2:
    st.header("Post History")
    try:
        df_history = pd.read_csv(HISTORY_FILE)
        st.dataframe(df_history)
    except Exception as e:
        st.warning("History file not found or unreadable.")

with tab3:
    st.header("Analytics Dashboard")
    try:
        df_analytics = pd.read_csv(ANALYTICS_FILE)
        st.dataframe(df_analytics)
    except Exception as e:
        st.warning("Analytics file not found or unreadable.")

with tab4:
    st.header("AI Descriptions")
    title = st.text_input("Track Title")
    sample_artist = st.text_input("Sample Artist")
    sample_title = st.text_input("Sample Title")
    if st.button("Generate Descriptions"):
        tags = generate_hashtags(title, sample_artist, sample_title)
        tag_str = " ".join(filter(None, tags))

        st.subheader("Instagram")
        st.code(f"{title} drop. Sampled from {sample_artist} – {sample_title}\n{tag_str}")

        st.subheader("TikTok")
        st.code(f"Flip of {sample_artist}. Can you guess the track?\n{tag_str}")

        st.subheader("YouTube")
        st.code(f"Boom Bap Beat: {title}\nSample: {sample_artist} – {sample_title}\n{tag_str}")

        st.subheader("Facebook")
        st.code(f"New beat this week: {title}\nFlip from {sample_title} by {sample_artist}\n{tag_str}")

        st.subheader("Shorts")
        st.code(f"{title} | Flip from {sample_artist}\n{tag_str}")
