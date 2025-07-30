import streamlit as st
from datetime import date, timedelta
import re
import pandas as pd
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Wantumeni Weekly Post Generator", layout="centered")
st.title("🎧 Wantumeni Post Generator")

# Files to store history
HISTORY_FILE = "post_history.csv"
ANALYTICS_FILE = "analytics.csv"

# Helper to delete rows
def delete_row(df, index):
    return df.drop(index=index).reset_index(drop=True)

# Calculate date ranges
today = date.today()
start_of_week = today - timedelta(days=today.weekday())
end_of_week = start_of_week + timedelta(days=6)
last_week_start = start_of_week - timedelta(days=7)
last_week_end = start_of_week - timedelta(days=1)

# Tabs for navigation
tab0, tab1, tab2, tab3 = st.tabs(["🏠 Home", "📄 Description", "📜 History", "📊 Analytics"])

with tab0:
    st.subheader("📊 Weekly Digest – This Week's Performance")
    if os.path.exists(ANALYTICS_FILE):
        df = pd.read_csv(ANALYTICS_FILE, parse_dates=["Date"])

        df_this_week = df[(df["Date"] >= pd.Timestamp(start_of_week)) & (df["Date"] <= pd.Timestamp(end_of_week))]
        df_last_week = df[(df["Date"] >= pd.Timestamp(last_week_start)) & (df["Date"] <= pd.Timestamp(last_week_end))]

        if not df_this_week.empty:
            top = df_this_week.sort_values("Reach", ascending=False).head(1).iloc[0]
            st.markdown(f"**🏆 Top Performer:** {top['Track Title']} on {top['Platform']} — {top['Reach']} Reach")

            totals = df_this_week.groupby("Platform")[["Reach", "Likes", "Saves"]].sum()
            st.markdown("**📈 Totals This Week by Platform:**")
            st.dataframe(totals)

            if not df_last_week.empty:
                reach_this = df_this_week["Reach"].sum()
                reach_last = df_last_week["Reach"].sum()
                growth = reach_this - reach_last
                pct = (growth / reach_last * 100) if reach_last > 0 else 0
                arrow = "⬆️" if growth >= 0 else "⬇️"
                st.markdown(f"**📊 Reach Growth vs Last Week:** {arrow} {growth} ({pct:.1f}%)")

            df_recent = df[df["Date"] >= pd.Timestamp(today - timedelta(days=28))].copy()
            df_recent["Week"] = df_recent["Date"].dt.to_period("W").astype(str)
            trend = df_recent.groupby("Week")["Reach"].sum()
            st.markdown("**📉 Reach Trend (Past 4 Weeks):**")
            st.line_chart(trend)
        else:
            st.info("No analytics entries found for this week.")
    else:
        st.info("No analytics data available yet.")

with tab1:
    st.markdown("Generate weekly post descriptions for all platforms.")

    track_title = st.text_input("Track Title")
    sample_artist = st.text_input("Sample Artist")
    sample_title = st.text_input("Sample Track")
    sample_year = st.text_input("Sample Year")
    youtube_url = st.text_input("YouTube URL (optional)")
    soundcloud_url = st.text_input("SoundCloud URL (optional)")

    core_tags = ['#boombap', '#hiphopinstrumental', '#beatmaker', '#akai', '#wantumeni']

    rotating_options = [
        '#lofi', '#sampling', '#samples', '#beats', '#beattape', '#hiphop', '#hiphopbeats',
        '#instrumental', '#soul', '#soulful', '#oldschool', '#cratedigger', '#vinyl'
    ]
    rotating_selected = st.multiselect("🎛️ Select up to 10 rotating tags:", options=rotating_options, max_selections=10)

    trendy_options = [
        '#typebeat', '#undergroundhiphop', '#instrumentals', '#musicproducer', '#drumbreaks', '#freestyletypebeat', '#jazzhop', '#90shiphop'
    ]
    trendy_selected = st.multiselect("🔥 Add trendy tags your audience is using:", options=trendy_options)

    format_option = st.radio("🔧 Choose tag format:", ["With #", "Without #", "Comma-separated"])

    sample_tag = f"#{re.sub(r'\\s+', '', sample_title.lower())}" if sample_title else ""
    artist_cleaned = re.sub(r'[^a-zA-Z0-9]', '', sample_artist.replace(' ', '')) if sample_artist else ""
    artist_tag = f"#{artist_cleaned.lower()}" if artist_cleaned else ""

    final_tags = core_tags + rotating_selected + trendy_selected + [sample_tag, artist_tag]

    if format_option == "Without #":
        display_tags = [tag.replace("#", "") for tag in final_tags]
    elif format_option == "Comma-separated":
        display_tags = ", ".join([tag.replace("#", "") for tag in final_tags])
    else:
        display_tags = " ".join(final_tags)

    linktree = "https://linktr.ee/wantumeni"

    if st.button("Generate Posts"):
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

    if track_title:
        st.markdown("---")
        st.subheader("📱 Mobile Preview")
        with st.container():
            st.markdown(f"""
            <div style='border:1px solid #ccc; border-radius:16px; padding:16px; max-width:360px; margin:auto; background:#fafafa;'>
                <strong>🎧 {track_title}</strong><br>
                <em>[unmastered demo]</em><br><br>
                Sample: {sample_artist} – {sample_title} ({sample_year})<br><br>
                🔁 Weekly beat drops<br>
                🎹 {display_tags}<br><br>
                🔗 {linktree}<br>
                📀 M.I.L.E. Music
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.subheader("📜 Post History")
    if os.path.exists(HISTORY_FILE):
        df_history = pd.read_csv(HISTORY_FILE)
        st.dataframe(df_history)
        selected_row = st.number_input("Select row to delete (by index)", min_value=0, max_value=len(df_history)-1, step=1)
        if st.button("Delete Selected Row"):
            df_history = delete_row(df_history, selected_row)
            df_history.to_csv(HISTORY_FILE, index=False)
            st.success("✅ Row deleted.")
            st.experimental_rerun()
        if st.button("📥 Download Post History (CSV)"):
            st.download_button("Download CSV", df_history.to_csv(index=False), file_name="post_history.csv")
    else:
        st.info("No post history saved yet.")

with tab3:
    st.subheader("📊 Analytics Tracker")
    with st.form("batch_analytics_form"):
        batch_date = st.date_input("Analytics Date", value=date.today())
        batch_title = st.text_input("Track Title for All Platforms")

        platforms = ["Instagram", "TikTok", "YouTube", "Facebook", "SoundCloud", "Other"]
        analytics_batch = []

        cols = st.columns(3)
        for i, platform in enumerate(platforms):
            with cols[i % 3]:
                st.markdown(f"**{platform}**")
                reach = st.text_input(f"Reach ({platform})", key=f"reach_{platform}")
                likes = st.text_input(f"Likes ({platform})", key=f"likes_{platform}")
                saves = st.text_input(f"Saves ({platform})", key=f"saves_{platform}")
                comments = st.text_input(f"Comments ({platform})", key=f"comments_{platform}")
                clicks = st.text_input(f"Clicks ({platform})", key=f"clicks_{platform}")
                analytics_batch.append({
                    "Date": batch_date,
                    "Platform": platform,
                    "Track Title": batch_title,
                    "Reach": reach,
                    "Likes": likes,
                    "Saves": saves,
                    "Comments": comments,
                    "Clicks": clicks
                })

        if st.form_submit_button("Save All Entries"):
            df_batch = pd.DataFrame(analytics_batch)
            if os.path.exists(ANALYTICS_FILE):
                df_existing = pd.read_csv(ANALYTICS_FILE)
                df_all = pd.concat([df_existing, df_batch], ignore_index=True)
            else:
                df_all = df_batch
            df_all.to_csv(ANALYTICS_FILE, index=False)
            st.success("✅ All analytics entries saved.")

    if os.path.exists(ANALYTICS_FILE):
        df_stats = pd.read_csv(ANALYTICS_FILE, parse_dates=["Date"])

        with st.expander("🔍 Filter Analytics"):
            track_filter = st.multiselect("Filter by Track Title:", options=df_stats["Track Title"].dropna().unique())
            platform_filter = st.multiselect("Filter by Platform:", options=df_stats["Platform"].dropna().unique())
            date_range = st.date_input("Select Date Range:", [df_stats["Date"].min(), df_stats["Date"].max()])

            if len(date_range) == 2:
                df_stats = df_stats[(df_stats["Date"] >= pd.Timestamp(date_range[0])) & (df_stats["Date"] <= pd.Timestamp(date_range[1]))]

            if track_filter:
                df_stats = df_stats[df_stats["Track Title"].isin(track_filter)]
            if platform_filter:
                df_stats = df_stats[df_stats["Platform"].isin(platform_filter)]

        st.dataframe(df_stats)

        try:
            df_stats["Reach"] = pd.to_numeric(df_stats["Reach"], errors="coerce")
            df_stats["Likes"] = pd.to_numeric(df_stats["Likes"], errors="coerce")
            df_stats["Engagement Rate"] = (df_stats["Likes"] / df_stats["Reach"] * 100).round(2)
            st.markdown("**📊 Engagement Rate (%):**")
            st.bar_chart(df_stats.groupby("Platform")["Engagement Rate"].mean())
        except:
            st.warning("⚠️ Could not calculate engagement rates. Check your data.")

        selected_a_row = st.number_input("Select analytics row to delete (by index)", min_value=0, max_value=len(df_stats)-1, step=1)
        if st.button("Delete Selected Analytics Row"):
            df_stats = delete_row(df_stats, selected_a_row)
            df_stats.to_csv(ANALYTICS_FILE, index=False)
            st.success("✅ Analytics row deleted.")
            st.experimental_rerun()

        if st.button("📥 Download Analytics (CSV)"):
            st.download_button("Download CSV", df_stats.to_csv(index=False), file_name="analytics.csv")
    else:
        st.info("No analytics data yet. Use the form above to log performance.")
