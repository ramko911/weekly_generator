import streamlit as st
from datetime import date
import re
import pandas as pd
import os

st.set_page_config(page_title="Wantumeni Weekly Post Generator", layout="centered")
st.title("🎧 Wantumeni Post Generator")
st.markdown("Generate weekly post descriptions for all platforms.")

# Files to store history
HISTORY_FILE = "post_history.csv"
ANALYTICS_FILE = "analytics.csv"

# Input fields
track_title = st.text_input("Track Title")
sample_artist = st.text_input("Sample Artist")
sample_title = st.text_input("Sample Track")
sample_year = st.text_input("Sample Year")
youtube_url = st.text_input("YouTube URL (optional)")
soundcloud_url = st.text_input("SoundCloud URL (optional)")

# Core hashtags
core_tags = ['#boombap', '#hiphopinstrumental', '#beatmaker', '#akai', '#wantumeni']

# Rotating tags
rotating_options = [
    '#lofi', '#sampling', '#samples', '#beats', '#beattape', '#hiphop', '#hiphopbeats',
    '#instrumental', '#soul', '#soulful', '#oldschool', '#cratedigger', '#vinyl'
]
rotating_selected = st.multiselect("🎛️ Select up to 10 rotating tags:", options=rotating_options, max_selections=10)

# Trendy tags dropdown
trendy_options = [
    '#typebeat', '#undergroundhiphop', '#instrumentals', '#musicproducer', '#drumbreaks', '#freestyletypebeat', '#jazzhop', '#90shiphop'
]
trendy_selected = st.multiselect("🔥 Add trendy tags your audience is using:", options=trendy_options)

# Format options
format_option = st.radio("🔧 Choose tag format:", ["With #", "Without #", "Comma-separated"])

# Generate dynamic tags from sample title and artist
sample_tag = f"#{re.sub(r'\\s+', '', sample_title.lower())}" if sample_title else ""
artist_cleaned = re.sub(r'[^a-zA-Z0-9]', '', sample_artist.replace(' ', '')) if sample_artist else ""
artist_tag = f"#{artist_cleaned.lower()}" if artist_cleaned else ""

# Combine all selected tags
final_tags = core_tags + rotating_selected + trendy_selected + [sample_tag, artist_tag]

if format_option == "Without #":
    display_tags = [tag.replace("#", "") for tag in final_tags]
elif format_option == "Comma-separated":
    display_tags = ", ".join([tag.replace("#", "") for tag in final_tags])
else:
    display_tags = " ".join(final_tags)

# CTA and links
linktree = "https://linktr.ee/wantumeni"

if st.button("Generate Posts"):
    # Sunday Meta / TikTok / Shorts
    sunday_meta = f"""
🎧 Boom Bap Hip Hop Instrumental – “{track_title}” by wantumeni  
[unmastered demo]

Sample:  
{sample_artist} – {sample_title} ({sample_year})

🔁 Weekly drops – Every Sunday  
🎹 {display_tags}  
📀 M.I.L.E. Music  

👉 Stream now via Linktree  
🔗 {linktree}
"""

    # Sunday YouTube
    sunday_youtube = f"""
🎧 wantumeni – “{track_title}” | Boom Bap Hip Hop Instrumental  
[unmastered demo]

Sample:  
{sample_artist} – {sample_title} ({sample_year})

🔁 Weekly beat drops – Sundays  
🎹 Raw boom bap / soulful samples / gritty drums  
📀 M.I.L.E. Music  

🔊 Stream & download:  
Linktree: {linktree}  
Instagram: https://instagram.com/wantumeni.x  
Soundcloud: https://soundcloud.com/wantumeni  
TikTok: https://tiktok.com/@wantumeni

{display_tags}
"""

    # Wednesday Meta / TikTok
    wednesday_meta = f"""
🎧 Missed it? “{track_title}” by wantumeni just dropped  
[unmastered demo] – Boom Bap Instrumental  

Sampled from:  
{sample_artist} – {sample_title} ({sample_year})

Now streaming on Soundcloud & YouTube  
🔗 {linktree}  

🔁 Weekly beat drops  
🎹 {display_tags}  
📀 M.I.L.E. Music
"""

    # Wednesday YouTube
    wednesday_youtube = f"""
🎧 New drop: “{track_title}” by wantumeni [unmastered demo]  
Boom Bap Hip Hop Instrumental  

Sampled from:  
{sample_artist} – {sample_title} ({sample_year})

Now available:  
🔗 YouTube: {youtube_url or '[URL]'}  
🔗 Soundcloud: {soundcloud_url or '[URL]'}  
🔗 All links: {linktree}  

🔁 Weekly beat drops  
🎹 Jazzy loops / gritty drums / classic vibe  
📀 M.I.L.E. Music  

{display_tags}
"""

    st.subheader("Sunday - Meta / TikTok / Shorts")
    st.code(sunday_meta, language='markdown')

    st.subheader("Sunday - YouTube")
    st.code(sunday_youtube, language='markdown')

    st.subheader("Wednesday - Meta / TikTok")
    st.code(wednesday_meta, language='markdown')

    st.subheader("Wednesday - YouTube")
    st.code(wednesday_youtube, language='markdown')

    st.subheader("📎 All Tags (Copy/Paste)")
    st.code(display_tags if isinstance(display_tags, str) else " ".join(display_tags))

    # Save history
    history_data = {
        "Date": date.today().isoformat(),
        "Title": track_title,
        "Sample Artist": sample_artist,
        "Sample Track": sample_title,
        "Sample Year": sample_year,
        "Tags": display_tags,
        "YouTube URL": youtube_url,
        "SoundCloud URL": soundcloud_url
    }
    df_new = pd.DataFrame([history_data])

    if os.path.exists(HISTORY_FILE):
        df_old = pd.read_csv(HISTORY_FILE)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new

    df_all.to_csv(HISTORY_FILE, index=False)
    st.success("✅ Post saved to history.")

# Load history view
st.markdown("---")
st.subheader("📜 Post History")
if os.path.exists(HISTORY_FILE):
    df_history = pd.read_csv(HISTORY_FILE)
    st.dataframe(df_history)
else:
    st.info("No post history saved yet.")

# Analytics Dashboard
st.markdown("---")
st.subheader("📊 Analytics Tracker")
with st.form("analytics_form"):
    a_date = st.date_input("Date", value=date.today())
    a_platform = st.selectbox("Platform", ["Instagram", "TikTok", "YouTube", "Facebook", "Other"])
    a_title = st.text_input("Associated Track Title (optional)")
    a_reach = st.text_input("Reach / Views")
    a_likes = st.text_input("Likes")
    a_saves = st.text_input("Saves")
    a_comments = st.text_input("Comments")
    a_clicks = st.text_input("Link Clicks (optional)")
    submitted = st.form_submit_button("Save Analytics Entry")

    if submitted:
        a_data = {
            "Date": a_date,
            "Platform": a_platform,
            "Track Title": a_title,
            "Reach": a_reach,
            "Likes": a_likes,
            "Saves": a_saves,
            "Comments": a_comments,
            "Clicks": a_clicks
        }
        df_analytics_new = pd.DataFrame([a_data])

        if os.path.exists(ANALYTICS_FILE):
            df_analytics_old = pd.read_csv(ANALYTICS_FILE)
            df_analytics_all = pd.concat([df_analytics_old, df_analytics_new], ignore_index=True)
        else:
            df_analytics_all = df_analytics_new

        df_analytics_all.to_csv(ANALYTICS_FILE, index=False)
        st.success("✅ Analytics entry saved.")

# Show analytics table
if os.path.exists(ANALYTICS_FILE):
    st.subheader("📈 Analytics Dashboard")
    df_stats = pd.read_csv(ANALYTICS_FILE)
    st.dataframe(df_stats)
else:
    st.info("No analytics data yet. Use the form above to log performance.")
