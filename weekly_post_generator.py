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

    title = st.text_input("Track Title")
    artist = st.text_input("Sample Artist")
    sample = st.text_input("Sample Title")
    year = st.text_input("Sample Year")
    youtube = st.text_input("YouTube URL")
    soundcloud = st.text_input("SoundCloud URL")
    linktree = st.text_input("Linktree URL", value="https://linktr.ee/wantumeni")

    format_style = st.radio("Hashtag Format", ["With #", "Without #", "Comma-separated"])

    hashtags = generate_platform_tags(title, artist, sample)["Instagram"]  # default tag set
    if format_style == "Without #":
        hashtags = [tag.replace('#', '') for tag in hashtags]
    elif format_style == "Comma-separated":
        hashtags = ", ".join([tag.replace('#', '') for tag in hashtags])
    else:
        hashtags = " ".join(hashtags)

    if st.button("Generate Preview"):
        st.subheader("Post Preview")
        st.markdown(f"**🎧 {title}** by wantumeni  ")
        st.markdown(f"Sample: {artist} – {sample} ({year})  ")
        st.markdown(f"🔁 Weekly drop  ")
        st.markdown(f"🎹 {hashtags}  ")
        st.markdown(f"🔗 [YouTube]({youtube}) | [SoundCloud]({soundcloud}) | [Linktree]({linktree})")

        post_data = {
            "Date": date.today().isoformat(),
            "Track Title": title,
            "Sample Artist": artist,
            "Sample Track": sample,
            "Sample Year": year,
            "YouTube": youtube,
            "SoundCloud": soundcloud,
            "Tags": hashtags
        }
        if os.path.exists(HISTORY_FILE):
            df = pd.read_csv(HISTORY_FILE)
            df = pd.concat([df, pd.DataFrame([post_data])], ignore_index=True)
        else:
            df = pd.DataFrame([post_data])
        df.to_csv(HISTORY_FILE, index=False)
        st.success("✅ Post saved to history.")

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
    title = st.text_input("Track Title (AI)", key="ai_title")
    artist = st.text_input("Sample Artist (AI)", key="ai_artist")
    sample = st.text_input("Sample Title (AI)", key="ai_sample")

    if st.button("Generate AI Descriptions"):
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
