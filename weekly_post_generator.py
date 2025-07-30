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

st.image("logo.svg", width=120)
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

# ... (rest of your script remains unchanged)

# This is a placeholder. The rest of your existing logic follows here unchanged.
# The visual update (logo + favicon) is all that's modified in this snippet.
