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

def clean_tag(text):
    return f"#{re.sub(r'[^a-zA-Z0-9]', '', text.replace(' ', '').lower())}" if text else ""

def generate_platform_tags(title, artist, sample):
    artist_tag = clean_tag(artist)
    sample_tag = clean_tag(sample)

    base = ["#boombap", "#hiphopinstrumental", "#beatmaker"]
    extra = ["#sampling", "#vinyl", "#soulful", "#typebeat"]

    return {
        "Instagram": base + [artist_tag, sample_tag] + ["#visuals", "#hiphopbeats"],
        "TikTok": base + [artist_tag, sample_tag] + ["#viralbeat", "#freestyle"],
        "YouTube": base + [artist_tag, sample_tag] + ["#instrumental", "#boombapbeats"],
        "Facebook": base + [artist_tag, sample_tag] + ["#musicproducer", "#beatdrop"],
        "Shorts": base + [artist_tag, sample_tag] + ["#shorts", "#musicshorts"]
    }

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
        tags = generate_platform_tags(title, artist, sample)

        st.subheader("Generated Hashtags")
        for platform, taglist in tags.items():
            st.markdown(f"**{platform}:** {' '.join([tag for tag in taglist if tag])}")

        st.subheader("Generated Descriptions")
        st.write(f"Instagram: New drop \"{title}\" sampling {sample} by {artist}! {' '.join(tags['Instagram'])}")
        st.write(f"YouTube Shorts: {title} flip out now! Beat inspired by {sample}. {' '.join(tags['Shorts'])}")
        st.write(f"TikTok: Cooking {title} with some {sample} vibes 🔥 {' '.join(tags['TikTok'])}")
        st.write(f"Facebook: \"{title}\" — soulful boom bap drop using {sample}. {' '.join(tags['Facebook'])}")
        st.write(f"YouTube: \"{title}\" by wantumeni | Sampled {artist} – {sample}. {' '.join(tags['YouTube'])}")
