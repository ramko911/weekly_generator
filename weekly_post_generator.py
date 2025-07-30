import streamlit as st
from datetime import date, timedelta
import pandas as pd
import re
import os

st.set_page_config(page_title="Wantumeni Post Generator", layout="centered")
st.title("🎧 Wantumeni Post Generator")

# File paths
HISTORY_FILE = "post_history.csv"
ANALYTICS_FILE = "analytics.csv"

# Helpers
def delete_row(df, index):
    return df.drop(index=index).reset_index(drop=True)

today = date.today()
start_of_week = today - timedelta(days=today.weekday())
end_of_week = start_of_week + timedelta(days=6)
last_week_start = start_of_week - timedelta(days=7)
last_week_end = start_of_week - timedelta(days=1)

# Navigation Tabs
tab0, tab1, tab2, tab3 = st.tabs(["🏠 Home", "📄 Description", "📜 History", "📊 Analytics"])

# --- HOME TAB --- #
with tab0:
    st.subheader("📊 Weekly Digest")
    if os.path.exists(ANALYTICS_FILE):
        df = pd.read_csv(ANALYTICS_FILE, parse_dates=["Date"])
        df_this = df[(df["Date"] >= pd.Timestamp(start_of_week)) & (df["Date"] <= pd.Timestamp(end_of_week))]
        df_last = df[(df["Date"] >= pd.Timestamp(last_week_start)) & (df["Date"] <= pd.Timestamp(last_week_end))]

        if not df_this.empty:
            top = df_this.sort_values("Reach", ascending=False).iloc[0]
            st.markdown(f"🏆 **Top Post**: {top['Track Title']} on {top['Platform']} – {top['Reach']} reach")
            st.markdown("### Totals by Platform")
            st.dataframe(df_this.groupby("Platform")[["Reach", "Likes", "Saves"]].sum())

            if not df_last.empty:
                delta = df_this["Reach"].sum() - df_last["Reach"].sum()
                pct = (delta / df_last["Reach"].sum() * 100) if df_last["Reach"].sum() else 0
                st.markdown(f"📈 **Growth vs Last Week**: {'⬆️' if delta >= 0 else '⬇️'} {delta} ({pct:.1f}%)")

            df_recent = df[df["Date"] >= pd.Timestamp(today - timedelta(days=28))].copy()
            df_recent["Week"] = df_recent["Date"].dt.to_period("W").astype(str)
            st.line_chart(df_recent.groupby("Week")["Reach"].sum())
        else:
            st.info("No entries yet for this week.")
    else:
        st.info("No analytics file found.")

# --- DESCRIPTION TAB --- #
with tab1:
    st.subheader("📝 Post Generator")

    title = st.text_input("Track Title")
    sample_artist = st.text_input("Sample Artist")
    sample_title = st.text_input("Sample Track")
    sample_year = st.text_input("Sample Year")
    yt_url = st.text_input("YouTube URL")
    sc_url = st.text_input("SoundCloud URL")

    core_tags = ['#boombap', '#hiphopinstrumental', '#beatmaker', '#akai', '#wantumeni']
    rotating = st.multiselect("Rotating Tags", [
        '#lofi', '#sampling', '#samples', '#beats', '#beattape', '#hiphop',
        '#hiphopbeats', '#instrumental', '#soul', '#oldschool', '#vinyl'
    ], max_selections=10)
    trendy = st.multiselect("Trendy Tags", [
        '#typebeat', '#undergroundhiphop', '#instrumentals', '#musicproducer', '#freestyletypebeat'
    ])
    tag_style = st.radio("Tag format", ["With #", "Without #", "Comma-separated"])

    sample_tag = f"#{re.sub(r'\\s+', '', sample_title.lower())}" if sample_title else ""
    artist_tag = f"#{re.sub(r'[^a-zA-Z0-9]', '', sample_artist.replace(' ', '').lower())}" if sample_artist else ""

    all_tags = core_tags + rotating + trendy + [sample_tag, artist_tag]
    if tag_style == "Without #":
        display_tags = [t.replace('#', '') for t in all_tags]
    elif tag_style == "Comma-separated":
        display_tags = ", ".join([t.replace('#', '') for t in all_tags])
    else:
        display_tags = " ".join(all_tags)

    linktree = "https://linktr.ee/wantumeni"

    if st.button("Generate Posts"):
        post_data = {
            "Date": date.today().isoformat(),
            "Title": title,
            "Sample Artist": sample_artist,
            "Sample Track": sample_title,
            "Sample Year": sample_year,
            "Tags": display_tags,
            "YouTube URL": yt_url,
            "SoundCloud URL": sc_url
        }
        df_new = pd.DataFrame([post_data])
        if os.path.exists(HISTORY_FILE):
            df_hist = pd.read_csv(HISTORY_FILE)
            df_all = pd.concat([df_hist, df_new], ignore_index=True)
        else:
            df_all = df_new
        df_all.to_csv(HISTORY_FILE, index=False)
        st.success("✅ Post saved!")

        st.markdown("### Preview")
        st.markdown(f"""
            **🎧 {title}** by wantumeni  
            Sample: {sample_artist} – {sample_title} ({sample_year})  
            🔁 Weekly drop  
            🎹 {display_tags}  
            🔗 {linktree}
        """)

# --- HISTORY TAB --- #
with tab2:
    st.subheader("📜 Post History")
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        st.dataframe(df)
        idx = st.number_input("Delete row (index)", min_value=0, max_value=len(df)-1)
        if st.button("Delete Selected Row"):
            df = delete_row(df, idx)
            df.to_csv(HISTORY_FILE, index=False)
            st.experimental_rerun()
        st.download_button("Download CSV", df.to_csv(index=False), file_name="post_history.csv")
    else:
        st.info("No post history yet.")

# --- ANALYTICS TAB --- #
with tab3:
    st.subheader("📊 Analytics Tracker")
    with st.form("analytics_batch"):
        d = st.date_input("Date", value=today)
        t = st.text_input("Track Title")
        p_list = ["Instagram", "TikTok", "YouTube", "Facebook", "SoundCloud", "Other"]
        analytics = []
        cols = st.columns(3)
        for i, platform in enumerate(p_list):
            with cols[i % 3]:
                st.markdown(f"**{platform}**")
                r = st.text_input(f"Reach ({platform})", key=f"r_{platform}")
                l = st.text_input(f"Likes ({platform})", key=f"l_{platform}")
                s = st.text_input(f"Saves ({platform})", key=f"s_{platform}")
                c = st.text_input(f"Comments ({platform})", key=f"c_{platform}")
                clk = st.text_input(f"Clicks ({platform})", key=f"clk_{platform}")
                analytics.append({"Date": d, "Platform": platform, "Track Title": t, "Reach": r, "Likes": l, "Saves": s, "Comments": c, "Clicks": clk})
        if st.form_submit_button("Save All"):
            df_batch = pd.DataFrame(analytics)
            if os.path.exists(ANALYTICS_FILE):
                df_old = pd.read_csv(ANALYTICS_FILE)
                df_all = pd.concat([df_old, df_batch], ignore_index=True)
            else:
                df_all = df_batch
            df_all.to_csv(ANALYTICS_FILE, index=False)
            st.success("✅ Analytics saved!")

    if os.path.exists(ANALYTICS_FILE):
        df = pd.read_csv(ANALYTICS_FILE, parse_dates=["Date"])
        with st.expander("Filter & Visualize"):
            tsel = st.multiselect("Track", df["Track Title"].dropna().unique())
            psel = st.multiselect("Platform", df["Platform"].dropna().unique())
            drange = st.date_input("Date range", [df["Date"].min(), df["Date"].max()])
            if len(drange) == 2:
                df = df[(df["Date"] >= pd.Timestamp(drange[0])) & (df["Date"] <= pd.Timestamp(drange[1]))]
            if tsel: df = df[df["Track Title"].isin(tsel)]
            if psel: df = df[df["Platform"].isin(psel)]

        st.dataframe(df)

        try:
            df["Reach"] = pd.to_numeric(df["Reach"], errors="coerce")
            df["Likes"] = pd.to_numeric(df["Likes"], errors="coerce")
            df["Engagement"] = (df["Likes"] / df["Reach"] * 100).round(2)
            st.bar_chart(df.groupby("Platform")["Engagement"].mean())
        except:
            st.warning("Engagement rate could not be calculated.")

        idx = st.number_input("Delete analytics row (index)", min_value=0, max_value=len(df)-1)
        if st.button("Delete Row"):
            df = delete_row(df, idx)
            df.to_csv(ANALYTICS_FILE, index=False)
            st.experimental_rerun()
        st.download_button("Download Analytics", df.to_csv(index=False), file_name="analytics.csv")
    else:
        st.info("No analytics entries yet.")
