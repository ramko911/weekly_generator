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

# Tab Navigation
tabs = st.tabs(["🏠 Home", "📄 Description", "📜 History", "📊 Analytics", "🪄 AI Descriptions"])

with tabs[0]:
    st.header("Weekly Digest")
    st.markdown("Top performer, engagement, trends, and insights coming soon.")

with tabs[1]:
    st.header("Post Description Generator")
    st.markdown("Form goes here to generate platform descriptions.")

with tabs[2]:
    st.header("Post History")
    try:
        df_history = pd.read_csv(HISTORY_FILE)
        st.dataframe(df_history)
    except:
        st.warning("History file not found or unreadable.")

with tabs[3]:
    st.header("Analytics Dashboard")
    try:
        df_analytics = pd.read_csv(ANALYTICS_FILE)
        st.dataframe(df_analytics)
    except:
        st.warning("Analytics file not found or unreadable.")

with tabs[4]:
    st.header("AI Descriptions")
    title = st.text_input("Track Title")
    artist = st.text_input("Sample Artist")
    sample = st.text_input("Sample Title")

    if st.button("Generate Descriptions"):
        hashtags = generate_hashtags(title, artist, sample)
        st.subheader("Generated Hashtags")
        st.write(" ".join([tag for tag in hashtags if tag]))
        st.subheader("Generated Descriptions")
        st.write(f"Instagram: New drop \"{title}\" sampling {sample} by {artist}! {' '.join(hashtags)}")
        st.write(f"YouTube Shorts: {title} flip out now! Beat inspired by {sample}. {' '.join(hashtags)}")
        st.write(f"TikTok: Cooking {title} with some {sample} vibes 🔥 {' '.join(hashtags)}")
