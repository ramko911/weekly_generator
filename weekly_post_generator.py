import streamlit as st
from datetime import date
import re

st.set_page_config(page_title="Wantumeni Weekly Post Generator", layout="centered")
st.title("🎧 Wantumeni Post Generator")
st.markdown("Generate weekly post descriptions for all platforms.")

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
